# SPEC file for EJBCA
The [official documentation](https://www.ejbca.org/docs/Installation_Instructions.html) tells to use 'ant' to build and install/deploy EJBCA.
The reason is that the properties files are part of the compiled Java archive.

As would Raymond Hettinger say:
> There must be a better way!

There is! You can build the Java archive in advance and deploy it as a RPM package.
It has the benefit of preventing mistakes in manual tasks and enforcing **the same** configuration on a farm of servers.

To build the RPM, you must have the following files in the SOURCES directory:
- ejbca_ee_<version_underlined>.zip (e.g. ejbca_ee_6_9_0_2.zip)
- ejbca-custom ([Official documentation](https://www.ejbca.org/docs/Customizing_EJBCA.html))
- <any_patch_you_want_to_apply>.diff

You must update the SPEC file to match the list of patches you want to apply.

## Deployment
Just create a symlink to /opt/ejbca/dist/ejbca.ear in the JBoss deployments directory.

## Different environments
If you have different environments (e.g. production + pre-production), just create 2 different SPEC files (e.g. ejbca-prod and ejbca-prep) based on this one.

## Different kinds of EJBCA installations
If you have different EJBCA instances (e.g. CA + OCSP responders), just create 2 different SPEC files (e.g. ejbca-ca and ejbca-ocsp) based on this one.
