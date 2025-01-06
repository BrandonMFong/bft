**x.x**
- [ ] include packages from other developers
- [ ] install specific versions
- [ ] [authenticate user](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app#using-the-device-flow-to-generate-a-user-access-token)
- [ ] make an easy installation process that can be called using something like `curl bft-install.brandonmfong.com | bash`
- [ ] add more data to the bucket files like author and descriptions
- [ ] add install and update progress

**0.2**
- [ ] apply standard python packaging layout
	- [ ] install bft in the home directory like goto?
- [ ] improve argument parser to detect incorrect arguments
- [ ] improve flag arguments so flags can be passed like `-afv`
- [ ] when downloading dmg, logic should be able to eject the dmg attached volume

**0.1**
- [x] improve list without fetching remote site
- [x] verbose argument
- [x] install a package
	- [x] download from given url
	- [x] read release version from the url
	- [x] download binary to an output folder
	- [x] install other tools
	- [x] support macos
- [x] tool update <bucket>
	- [x] check for updates
- [x] uninstall
- [x] ability to list available packages
- [x] make a separate repo as a registry

