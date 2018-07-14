# Static LibreSSL RPM

## Intended Use

The RPM build from the spec file will provide static libraries for LibreSSL.  This enables applications that have build requirements on LibreSSL (that statically link) to be compiled within an isolated environment.

## Hobbled

Like the OpenSSL offerings for RHEL/CentOS/Fedora, this similarly uses a hobble script (`hobble-libressl`) to remove patented or encumbered code, namely EC2m.

### How To Hobble

1. Fetch the latest [LibreSSL release](https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/).
2. Extract the archive
3. Copy `hobble-libressl` into the root of LibreSSL and execute.

## Building

After you've hobbled the LibreSSL release, archive the source as a `libressl-<version>-hobbled.tar.gz`and place in `~/rpmbuild/SOURCES`.

```
git clone https://github.com/rsclarke/libressl-static-rpm.git
cd libressl-static-rpm
cp libressl.spec ~/rpmbuild/SPECS
cp *.patch ~/rpmbuild/SOURCES
rpmbuild -bs ~/rpmbuild/SPECS/libressl.spec
mock rebuild ~/rpmbuild/SRPMS/libressl-<version>.<env>.src.rpm
```
