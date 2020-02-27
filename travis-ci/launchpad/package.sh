#!/bin/sh

# Exit on errors
set -e

. "${TRAVIS_BUILD_DIR}/travis-ci/defs.sh"

print_headline "Packaging for Launchpad"

GIT_HASH=$(git --git-dir=".git" show --no-patch --pretty="%h")
GIT_DATE=$(git --git-dir=".git" show --no-patch --pretty="%ci")
DATE_HASH=$(date -u +"%Y%m%d%H%M")
VERSION="0.1.1"
VERSION_NAME="${VERSION}-${DATE_HASH}-git_${GIT_HASH}"


DEBDATE=$(date -R)

echo_var "GIT_HASH"
echo_var "GIT_DATE"
echo_var "VERSION_NAME"
echo_var "DEBDATE"
echo_var "DEB_MAINTAINER_NAME"
echo_var "DEB_MAINTAINER_EMAIL"
echo_var "LAUNCHPAD_DISTROS"

if [ -z "${DEB_MAINTAINER_NAME}" -o -z "${DEB_MAINTAINER_EMAIL}" -o -z "${DEB_PASSPHRASE}" -o -z "${LAUNCHPAD_DISTROS}" ]; then
	print_error "DEB_MAINTAINER_NAME and/or DEB_MAINTAINER_EMAIL and/or DEB_PASSPHRASE and/or LAUNCHPAD_DISTROS are not set"
	exit 0
fi

print_info "Decrypt keys"
cd "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/"
openssl aes-256-cbc -K $encrypted_e8757174037a_key -iv $encrypted_e8757174037a_iv -in keys.tar.enc -out keys.tar -d
tar xvf keys.tar
cd "${TRAVIS_BUILD_DIR}"

print_info "Import signing key"
gpg --import "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/key.asc"


print_info "Add ppa.launchpad.net to known hosts"
# Add ppa.launchpad.net to ssh's known hosts so we can upload to it using sftp
echo "ppa.launchpad.net ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0aKz5UTUndYgIGG7dQBV+HaeuEZJ2xPHo2DS2iSKvUL4xNMSAY4UguNW+pX56nAQmZKIZZ8MaEvSj6zMEDiq6HFfn5JcTlM80UwlnyKe8B8p7Nk06PPQLrnmQt5fh0HmEcZx+JU9TZsfCHPnX7MNz4ELfZE6cFsclClrKim3BHUIGq//t93DllB+h4O9LHjEUsQ1Sr63irDLSutkLJD6RXchjROXkNirlcNVHH/jwLWR5RcYilNX7S5bIkK8NlWPjsn/8Ua5O7I9/YoE97PpO6i73DTGLh5H9JN/SITwCKBkgSDWUt61uPK3Y11Gty7o2lWsBjhBUm2Y38CBsoGmBw==" >> ~/.ssh/known_hosts

print_info "Creating ~/.ssh/config"
echo """Host ppa.launchpad.net
IdentityFile ${TRAVIS_BUILD_DIR}/travis-ci/launchpad/id_rsa_texworks
User st.loeffler
""" >> ~/.ssh/config

for DISTRO in ${LAUNCHPAD_DISTROS}; do
	print_info "Packging for ${DISTRO}"
	echo -n "   "

	ORIG_VERSION=$(echo "${VERSION_NAME}" | tr "_-" "~")
	ORIGNAME="texworks-help_${ORIG_VERSION}"
	DEB_VERSION="${ORIG_VERSION}-1${DISTRO}"
	DEBNAME="texworks-help_${DEB_VERSION}"
	DEBDIR="${DEBNAME}"
	echo_var "DEB_VERSION"

	print_info "   exporting sources to ${DEBDIR}"
	mkdir -p "${DEBDIR}"
	cd "${TRAVIS_BUILD_DIR}" && git archive --prefix="${ORIGNAME}/" --output="${ORIGNAME}.orig.tar.gz" HEAD
	tar -x -C "${DEBDIR}" --strip-components=1 -f "${ORIGNAME}.orig.tar.gz"

	print_info "   copying debian directory"
	cp -r "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/debian" "${DEBDIR}"

	if [ -f "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/${DISTRO}.patch" ]; then
		print_info "   applying ${DISTRO}.patch"
		patch -d "${DEBDIR}" -p0 < "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/${DISTRO}.patch"
	fi

	print_info "   preparing copyright"
	sed -i -e "s/<AUTHOR>/${DEB_MAINTAINER_NAME}/g" -e "s/<DATE>/${DEBDATE}/g" "${DEBDIR}/debian/copyright"

	print_info "   preparing changelog"
	echo "texworks-help (${DEB_VERSION}) ${DISTRO}; urgency=low\n" > "${DEBDIR}/debian/changelog"
	if [ -z "${TRAVIS_TAG}" ]; then
		git log --reverse --pretty=format:"%w(80,4,6)* %s" ${TRAVIS_COMMIT_RANGE} >> "${DEBDIR}/debian/changelog"
		echo "" >> "${DEBDIR}/debian/changelog" # git log does not append a newline
	else
		NEWS=$(sed -n "/^Release ${VERSION}/,/^Release/p" ${TRAVIS_BUILD_DIR}/NEWS | sed -e '/^Release/d' -e 's/^\t/    /')
		echo "$NEWS" >> "${DEBDIR}/debian/changelog"
	fi
	echo "\n -- ${DEB_MAINTAINER_NAME} <${DEB_MAINTAINER_EMAIL}>  ${DEBDATE}" >> "${DEBDIR}/debian/changelog"
	
	print_info "   building package"
	cd "${DEBDIR}"

	echo -n "" > "/tmp/passphrase.txt" || print_error "Failed to create /tmp/passphrase.txt"
	# Write the passphrase to the file several times; debuild (debsign)
	# will try to sign (at least) the .dsc file and the .changes files,
	# thus reading the passphrase from the pipe several times
	# NB: --passphrase-file seems to be broken somehow
	for i in $(seq 10); do
		echo "${DEB_PASSPHRASE}" >> "/tmp/passphrase.txt" 2> /dev/null || print_error "Failed to write to /tmp/passphrase.txt"
	done
	debuild -k00582F84 -p"gpg --no-tty --batch --passphrase-fd 0" -S < /tmp/passphrase.txt && DEBUILD_RETVAL=$? || DEBUILD_RETVAL=$?
	rm -f /tmp/passphrase.txt

	if [ $DEBUILD_RETVAL -ne 0 ]; then
		print_warning "   debuild failed with status code ${DEBUILD_RETVAL}"
		continue
	fi
	cd ..

	DEBFILE="${DEBNAME}_source.changes"
	if [ -z "${TRAVIS_TAG}" ]; then
		PPA="tw-latest"
	else
		PPA="tw-stable"
	fi
	print_info "   scheduling to upload ${DEBFILE} to ${PPA}"

	echo "dput --config \"${TRAVIS_BUILD_DIR}/travis-ci/launchpad/dput.cf\" \"${PPA}\" \"${TRAVIS_BUILD_DIR}/${DEBFILE}\"" >> "${TRAVIS_BUILD_DIR}/travis-ci/launchpad/dput-launchpad.sh"
done
