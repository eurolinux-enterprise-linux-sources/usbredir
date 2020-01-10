Name:           usbredir
Version:        0.5.1
Release:        2%{?dist}
Summary:        USB network redirection protocol libraries
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://spice-space.org/page/UsbRedir
Source0:        http://spice-space.org/download/%{name}/%{name}-%{version}.tar.bz2
Patch1:         0001-usbredirparser-Update-header-len-inside-the-usbredir.patch
Patch2:         0001-usbredirhost-Add-a-do-not-reset-device-blacklist.patch
BuildRequires:  libusb1-devel >= 1.0.9
ExcludeArch:    s390 s390x

%description
usbredir is a protocol for redirection USB traffic from a single USB device,
to a different (virtual) machine then the one to which the USB device is
attached. This package contains a number of libraries to help implementing
support for usbredir:

usbredirparser:
A library containing the parser for the usbredir protocol

usbredirhost:
A library implementing the usb-host side of a usbredir connection.
All that an application wishing to implement an usb-host needs to do is:
* Provide a libusb device handle for the device
* Provide write and read callbacks for the actual transport of usbredir data
* Monitor for usbredir and libusb read/write events and call their handlers


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        server
Summary:        Simple usb-host tcp server
Group:          System Environment/Daemons
License:        GPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
A simple usb-host tcp server, using libusbredirhost.


%prep
%setup -q
%patch1 -p1
%patch2 -p1


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libusbredir*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING.LIB README TODO 
%{_libdir}/libusbredir*.so.*

%files devel
%defattr(-,root,root,-)
%doc usb-redirection-protocol.txt README.multi-thread
%{_includedir}/usbredir*.h
%{_libdir}/libusbredir*.so
%{_libdir}/pkgconfig/libusbredir*.pc

%files server
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/usbredirserver
%{_mandir}/man1/usbredirserver.1*


%changelog
* Mon Mar  2 2015 Hans de Goede <hdegoede@redhat.com> - 0.5.1-2
- Add upstream patch to fix usbredirparser headerlen bug when talking to
  the standalone usbredirserver
- Resolves: rhbz#1085318
- Add upstream patch with do-not-reset-device-blacklist
- Extend blacklist with 2798:0001
- Resolves: rhbz#1115917

* Wed Sep 19 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.1-1
- Update to upstream 0.5.1 release
- Resolves: rhbz#842356
- Remove bulk packets time out, this fixes various devices not working
- Resolves: rhbz#834560
- Add support to libusbredirparser for state serialization
- Resolves: rhbz#842316
- Drop isochronous packets when the network is too slow to keep up
- Resolves: rhbz#855737

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.3-1
- Update to upstream 0.4.3 release
- Don't crash on devices in unconfigured state
- Resolves: rhbz#808758
- Significantly speed up reset handling
- Resolves: rhbz#808730

* Tue Mar  6 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.2-1
- Update to upstream 0.4.2 release
- Related: rhbz#758098

* Sat Feb 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to upstream 0.4.1 release
- Related: rhbz#758098

* Thu Feb 23 2012 Hans de Goede <hdegoede@redhat.com> - 0.4-1
- Update to upstream 0.4 release
- Related: rhbz#758098

* Wed Jan 18 2012 Hans de Goede <hdegoede@redhat.com> - 0.3.3-3
- Add ExcludeArch: s390 s390x as there is no libusb there 
- Related: rhbz#758098

* Tue Jan 17 2012 Hans de Goede <hdegoede@redhat.com> - 0.3.3-2
- Build for RHEL-6
- Resolves: rhbz#758098

* Thu Jan 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.3.3-1
- Update to upstream 0.3.3 release

* Tue Jan  3 2012 Hans de Goede <hdegoede@redhat.com> 0.3.2-1
- Update to upstream 0.3.2 release

* Wed Aug 24 2011 Hans de Goede <hdegoede@redhat.com> 0.3.1-1
- Update to upstream 0.3.1 release

* Thu Jul 14 2011 Hans de Goede <hdegoede@redhat.com> 0.3-1
- Initial Fedora package
