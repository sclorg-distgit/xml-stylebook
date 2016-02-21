%global pkg_name xml-stylebook
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:          %{?scl_prefix}%{pkg_name}
Version:       1.0
Release:       0.14.b3_xalan2.svn313293.14%{?dist}
Summary:       Apache XML Stylebook
License:       ASL 1.1
URL:           http://xml.apache.org/

# How to generate this tarball:
#  $ svn export http://svn.apache.org/repos/asf/xml/stylebook/trunk/@313293 xml-stylebook-1.0
#  $ rm -rf xml-stylebook-1.0/bin/* # unclear licensing
#  $ rm -rf xml-stylebook-1.0/styles/ibm-style # better not to include the logos
#  $ tar zcf xml-stylebook-1.0.tar.gz xml-stylebook-1.0
Source0:       %{pkg_name}-%{version}.tar.gz

# Patch to fix an NPE in Xalan-J2's docs generation (from JPackage)
Patch0:        %{pkg_name}-image-printer.patch

# Patch the build script to build javadocs
Patch1:        %{pkg_name}-build-javadoc.patch

BuildArch:     noarch

BuildRequires: %{?scl_prefix_java_common}javapackages-tools
BuildRequires: %{?scl_prefix_java_common}ant
BuildRequires: %{?scl_prefix_java_common}xml-commons-apis
BuildRequires: %{?scl_prefix_java_common}xerces-j2
BuildRequires: dejavu-sans-fonts
BuildRequires: fontconfig
Requires:      %{?scl_prefix_java_common}xml-commons-apis
Requires:      %{?scl_prefix_java_common}xerces-j2
%{?scl:Requires: %{scl_prefix}runtime}

%description
Apache XML Stylebook is a HTML documentation generator.

%package       javadoc
Summary:       API documentation for %{pkg_name}

%description   javadoc
%{summary}.

%package       demo
Summary:       Examples for %{pkg_name}
Requires:      %{name} = %{version}-%{release}

%description   demo
Examples demonstrating the use of %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p0
%patch1 -p0

# Don't include this sample theme because it contains an errant font
rm -r styles/christmas/

# Make sure upstream hasn't sneaked in any jars we don't know about
JARS=""
for j in `find -name "*.jar"`; do
  if [ ! -L $j ]; then
    JARS="$JARS $j"
  fi
done
if [ ! -z "$JARS" ]; then
   echo "These jars should be deleted and symlinked to system jars: $JARS"
   exit 1
fi
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath xalan-j2 xerces-j2)
ant

# Build the examples (this serves as a good test suite)
pushd docs
rm run.bat
java -classpath "$(build-classpath xml-commons-apis):$(build-classpath xerces-j2):../bin/stylebook-%{version}-b3_xalan-2.jar" \
  org.apache.stylebook.StyleBook "targetDirectory=../results" book.xml ../styles/apachexml
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# jars
install -pD -T bin/stylebook-%{version}-b3_xalan-2.jar \
  %{buildroot}%{_javadir}/%{pkg_name}.jar

# javadoc
install -d %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# examples
install -d %{buildroot}%{_datadir}/%{pkg_name}
cp -pr docs %{buildroot}%{_datadir}/%{pkg_name}
cp -pr styles %{buildroot}%{_datadir}/%{pkg_name}
cp -pr results %{buildroot}%{_datadir}/%{pkg_name}
%{?scl:EOF}

%files
%doc LICENSE.txt
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{pkg_name}

%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.14
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.13
- maven33 rebuild

* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.12
- Add missing requires on maven30-runtime

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.11
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.10
- Fix BR/R

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.9
- Mass rebuild 2015-01-06

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.8
- Add BuildRequires on fontconfig
- Resolves: rhbz#1101587

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.14.b3_xalan2.svn313293.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0-0.14.b3_xalan2.svn313293
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-0.13.b3_xalan2.svn313293
- Cleanup tarball content with unclear license
- Update to latest packaging guidelines

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.12.b3_xalan2.svn313293
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.11.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.10.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.7.b3_xalan2.svn313293
- Really fix FTBFS this time.

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.6.b3_xalan2.svn313293
- Fix FTBFS due to ant upgrade.

* Sat Jun 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.5.b3_xalan2.svn313293
- Link to local java API docs properly and fix requires on javadoc package.
- Build with source and target levels of 1.5 so we don't have to require 1.6.

* Mon Apr 22 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.4.b3_xalan2.svn313293
- Remove font from demo package to comply with guidelines. RHBZ #567912

* Mon Jan 11 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.3.b3_xalan2.svn313293
- Build the examples (this serves as a good test suite.)
- Patch the build script to build javadocs.
- Add a build dep on a font package because the JDK is missing a dependency
  to function correctly in headless mode. See RHBZ #478480 and #521523.

* Tue Jan 5 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.2.b3_xalan2.svn313293
- Add patch from JPackage to fix NPE in Xalan-J2 doc generation.

* Tue Jan 5 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.1.b3_xalan2.svn313293
- Initial stab at packaging trunk version of stylebook.
