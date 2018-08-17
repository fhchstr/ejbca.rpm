# SPEC file for EJBCA
The [official documentation](https://www.ejbca.org/docs/Installation_Instructions.html) tells to use 'ant' to build and install/deploy EJBCA.
The reason for it is that the properties files are part of the compile Java archive.

As would Raymond Hettinger say:
> There must be a better way!

There is! You can build the Java archive in advance and deploy it as a RPM package.
It has the benefit of preventing mistakes in manual tasks and enforcing **the same** configuration on a farm of servers.

You must have the following files in the SOURCES directory:
- ejbca_ee_<version_underlined>.zip (e.g. ejbca_ee_6_9_0_2.zip)
- ejbca-custom ([Official documentation](https://www.ejbca.org/docs/Customizing_EJBCA.html))
- <any_patch_you_want_to_apply>.diff

You must update the SPEC file to match the list of patches you want to apply.

## Different environments
The same SPEC file can be used to build different RPMs for each platform.
As an example, it checks if a file called .build_prep exists. If yes, it builds the package for pre-production. If not, for production.
Edit this logic to match your needs.

## Deployment
Just create a symlink to /opt/ejbca/dist/ejbca.ear in the JBoss deployments directory.

## Different kinds of EJBCA installations
If you have different EJBCA instances (e.g. CA + OCSP responders), just create 2 different SPEC files (e.g. ejbca-ca and ejbca-ocsp) based on this one.
