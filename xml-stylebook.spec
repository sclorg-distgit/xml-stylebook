%{?scl:%scl_package xml-stylebook}
%{!?scl:%global pkg_name %{name}}

Name:          %{?scl_prefix}xml-stylebook
Version:       1.0
Release:       0.21.b3_xalan2.svn313293.2%{?dist}
Summary:       Apache XML Stylebook
License:       ASL 1.1
URL:           http://xml.apache.org/

# How to generate this tarball:
#  $ svn export http://svn.apache.org/repos/asf/xml/stylebook/trunk/@313293 xml-stylebook-1.0
#  $ tar zcf xml-stylebook-1.0.tar.gz xml-stylebook-1.0
Source0:       %{pkg_name}-%{version}.tar.gz

# Patch to fix an NPE in Xalan-J2's docs generation (from JPackage)
Patch0:        %{pkg_name}-image-printer.patch

# Patch the build script to build javadocs
Patch1:        %{pkg_name}-build-javadoc.patch

BuildArch:     noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: %{?scl_prefix}javapackages-local
BuildRequires: %{?scl_prefix}ant
BuildRequires: %{?scl_prefix}xml-commons-apis
BuildRequires: %{?scl_prefix}xerces-j2
BuildRequires: dejavu-sans-fonts
Requires:      java-headless
Requires:      %{?scl_prefix}xml-commons-apis
Requires:      %{?scl_prefix}xerces-j2

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
%setup -n %{pkg_name}-%{version} -q
%patch0 -p0
%patch1 -p0

# Remove bundled binaries
find -name *.jar -delete

# Don't include this sample theme because it contains an errant font
rm -r styles/christmas/

%build
ant -Dclasspath=$(build-classpath xml-commons-apis xerces-j2)

# Build the examples (this serves as a good test suite)
pushd docs
rm run.bat
java -classpath "$(build-classpath xml-commons-apis xerces-j2):../bin/stylebook-%{version}-b3_xalan-2.jar" \
  org.apache.stylebook.StyleBook "targetDirectory=../results" book.xml ../styles/apachexml
popd

%install
# jars
install -pD -T bin/stylebook-%{version}-b3_xalan-2.jar \
  %{buildroot}%{_javadir}/%{pkg_name}.jar

# javadoc
install -d %{buildroot}%{_javadocdir}/%{pkg_name}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{pkg_name}

# examples
install -d %{buildroot}%{_datadir}/%{pkg_name}
cp -pr docs %{buildroot}%{_datadir}/%{pkg_name}
cp -pr styles %{buildroot}%{_datadir}/%{pkg_name}
cp -pr results %{buildroot}%{_datadir}/%{pkg_name}

%files
%license LICENSE.txt
%{_javadir}/*

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{pkg_name}

%files demo
%{_datadir}/%{pkg_name} 

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 1.0-0.21.b3_xalan2.svn313293.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.0-0.21.b3_xalan2.svn313293.1
- Automated package import and SCL-ization

* Thu Mar 30 2017 Mat Booth <mat.booth@redhat.com> - 1.0-0.21.b3_xalan2.svn313293
- Fix FTBFS and javadoc linting errors
- Adopt license macro

* Fri Mar  3 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.20.b3_xalan2.svn313293
- Update to current packaging guidelines

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.19.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.18.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.17.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.16.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-0.15.b3_xalan2.svn313293
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.14.b3_xalan2.svn313293
- Prefer xerces-j2 instead of gcj for providing jaxp_parser_impl

* Sat Aug 10 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.13.b3_xalan2.svn313293
- Update for newer guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.12.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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

* Thu Apr 22 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.4.b3_xalan2.svn313293
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
