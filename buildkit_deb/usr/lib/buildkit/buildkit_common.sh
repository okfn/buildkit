#
# General functions
#

buildkit_ensure_buildkit_directories () {
    if [ $# -lt 1 ]
    then
        echo "Not enough arguments"
        exit 1
    fi
    BASEDIR=$1
    mkdir -p -m 0750 ${BASEDIR}/{,/vm,/repo,/vmtmp}
    mkdir -p -m 0750 /var/log/buildkit/

}

buildkit_ensure_permissions (){
    sudo chown -R buildkit:www-data /var/log/buildkit/ 
    sudo chmod -R g+w /var/log/buildkit/ 
    sudo chown -R buildkit:www-data /var/lib/buildkit/ 
    sudo chmod -R g+r /var/lib/buildkit/ 
}

#
# Dist Functions
#

buildkit_ensure_dist_deps () {
    echo "Skipping git-flow install."
#sudo ./usr/bin/buildkit-gitflow-installer
}

buildkit_ensure_hosts () {
    COMMAND_OUTPUT=`cat /etc/hosts | grep "default.vm.buildkit"`
    if ! [[ "$COMMAND_OUTPUT" =~ "default.vm.buildkit" ]] ; then
        echo "Adding default.vm.buildkit to /etc/hosts  ..."
        cat << EOF | sudo tee -a /etc/hosts
192.168.100.10 default.vm.buildkit
EOF
    fi
}

buildkit_ensure_user_and_group () {
    local INSTANCE
    COMMAND_OUTPUT=`cat /etc/group | grep "buildkit:"`
    if ! [[ "$COMMAND_OUTPUT" =~ "buildkit:" ]] ; then
        echo "Creating the 'buildkit' group ..."
        sudo groupadd --system "buildkit"
    fi
    COMMAND_OUTPUT=`cat /etc/passwd | grep "buildkit:"`
    if ! [[ "$COMMAND_OUTPUT" =~ "buildkit:" ]] ; then
        echo "Creating the 'buildkit' user ..."
        sudo useradd  --system  --gid "buildkit" --home /var/lib/buildkit/ -M  --shell /usr/sbin/nologin buildkit
    fi
}

buildkit_ensure_public_key() {
    if [ $# -lt 5 ]
    then
        echo "Not enough arguments"
        exit 1
    fi
    NAME=$1
    EMAIL=$2
    COMMENT=$3
    KEYDIR=$4
    REPOBASE=$5
    mkdir -p $REPOBASE
    if [ ! -e "$REPOBASE/package_public.key" ]
    then
        #sudo -u buildkit mkdir -p $REPOBASE
        echo "Creating key in $KEYDIR with name $NAME, email $EMAIL, comment $COMMENT ..."
        # Check we haven't already created the home directory
        if [ ! -d "$KEYDIR" ]
        then
            echo "Working to create $KEYDIR ..."
            mkdir $KEYDIR
            chmod 700 $KEYDIR
            # Note the tabs begining the lines below are important and cannot be replaced by spaces
            cat > ${KEYDIR}/buildkit_settings <<- EOF
	%echo Generating a basic OpenPGP key for buildkit, THIS CAN TAKE A FEW MINUTES if there is not enough entropy ...
	Key-Type: DSA
	Key-Length: 1024
	Subkey-Type: ELG-E
	Subkey-Length: 1024
	Name-Real: $NAME
	Name-Comment: $COMMENT
	Name-Email: $EMAIL
	Expire-Date: 0
	# Note that we choose to use a passwordless key here and ignore the password option
        %no-protection
	#Passphrase: $PASSWORD
	%pubring ${KEYDIR}/buildkit.pub
	%secring ${KEYDIR}/buildkit.sec
	# Do a commit here, so that we can later print "done" :-)
	%commit
	%echo done
	EOF
            echo "Generating the key (as $USER) ..."
            echo "Going to run: gpg --batch --gen-key ${KEYDIR}/buildkit_settings; rm ${KEYDIR}/buildkit_settings; gpg --homedir ${KEYDIR} --allow-secret-key-import --import ${KEYDIR}/buildkit.sec; gpg --armor --keyring ${KEYDIR}/buildkit.pub --secret-keyring ${KEYDIR}/buildkit.sec --output ${REPOBASE}/packages_public.key --export $EMAIL;"
            gpg --batch --gen-key ${KEYDIR}/buildkit_settings
            rm ${KEYDIR}/buildkit_settings
            gpg --homedir ${KEYDIR} --allow-secret-key-import --import ${KEYDIR}/buildkit.sec
            echo "Exporting the key ..."
            gpg --armor --keyring ${KEYDIR}/buildkit.pub --secret-keyring ${KEYDIR}/buildkit.sec --output ${REPOBASE}/packages_public.key --export $EMAIL
            #chown buildkit:www-data ${REPOBASE}/packages_public.key
            #chmod g+r ${REPOBASE}/packages_public.key
        fi
    fi
}

buildkit_ensure_base_repo() {
    if [ $# -lt 2 ]
    then
        echo "Not enough arguments"
        exit 1
    fi
    REPOBASE=$1
    NAME=$2
    if [ ! -d ${REPOBASE}/base ]
    then
        echo "Creating the base lucid repository ..."
        mkdir -p ${REPOBASE}/base_lucid/conf
        cat > ${REPOBASE}/base_lucid/conf/distributions <<- EOF
	Origin: $NAME
	Label: $NAME
	Codename: lucid
	Architectures: i386 amd64 source
	Components: universe
	Description: $NAME
	SignWith: yes
	DebOverride: override.lucid
	DscOverride: override.lucid
	EOF
        touch ${REPOBASE}/base_lucid/conf/override.lucid
        cat > ${REPOBASE}/base_lucid/conf/options <<- EOF
	verbose
	ask-passphrase
	basedir .
	EOF
        sudo chown -R buildkit:www-data ${REPOBASE}
        sudo chmod -R g+r ${REPOBASE}
    fi
}

buildkit_ensure_apache() {
    if [ $# -lt 1 ]
    then
        echo "Not enough arguments"
        exit 1
    fi
    REPOBASE=$1
    cat <<- EOF > /etc/apache2/sites-available/buildkit-repo
	<VirtualHost *:80>
	    # WARNING: Do not manually edit this file, it is desgined to be 
	    #          overwritten at any time by the postinst script of 
	    #          dependent packages
	
	    DocumentRoot $REPOBASE
	    ServerName host.buildkit
	
	    <LocationMatch "/(.*)/conf" >
	        deny from all
	    </LocationMatch>
	
	    <LocationMatch "/(.*)/db" >
	        deny from all
	    </LocationMatch>
	</VirtualHost>
	EOF
    sudo a2ensite buildkit-repo
    sudo /etc/init.d/apache2 reload
}

buildkit_ensure_apt_cacher() {
    echo "Writing to /etc/apt-cacher-ng/ubuntu_security ..."
    cat <<- EOF > /etc/apt-cacher-ng/ubuntu_security
	http://security.ubuntu.com/ubuntu
	EOF
    echo "done."
    echo "Updating /etc/apt-cacher-ng/acng.conf ..."
    sed -e "s,; file:backends_debvol, ;  file:backends_debvol\nRemap-ubusec: file:ubuntu_security /ubuntu-security ; http://security.ubuntu.com/ubuntu," \
                -i /etc/apt-cacher-ng/acng.conf
        #-e "s,Port:3142,Port:9999," \
    echo "done."
}
