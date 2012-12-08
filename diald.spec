Summary:	Daemon that provides on demand IP links via SLIP or PPP
Name:		diald
Version:	1.0
Release:	19
License:	GPL
Url:		http://diald.sourceforge.net
Group:		Networking/Other
Source0:	%{name}-%{version}.tar.bz2
Source1:	diald.init
Source2:	diald.conf
Source3:	diald.filter
Patch3:		diald-c-files.patch
Patch4:		diald-1.0.patch
Patch5:		diald-1.0-fix-glibc2.4.patch
Requires:	ppp
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description
Diald is a daemon that provides on demand IP links via SLIP or PPP. The
purpose of diald is to make it transparently appear that you have a
permanent connection to a remote site. Diald sets up a "proxy" device which
stands in for the physical connection to a remote site. It then monitors the
proxy, waiting for packets to arrive. When interesting packets arrive it
will attempt to establish the physical link to the remote site using either
SLIP or PPP, and if it succeeds it will forward traffic from the proxy to
the physical link. As well, diald will monitor traffic once the physical
link is up, and when it has determined that the link is idle, the remote
connection is terminated. The criteria for bringing the link up and taking
it down are configurable at run time, and are based upon the type of traffic
passing over the link.

Note that even if you use ppp for your connections, you still need slip 
compiled, either into the kernel or as a module.

%prep
%setup -q
%patch3 -p0
%patch4 -p1 -b .mdk
%patch5 -p1 -b .glibc2.4

%build
%configure2_5x	--localstatedir=/var
make

%install
%makeinstall_std

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/diald
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/diald/diald.conf
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/diald/diald.filter
mkdir -p %{buildroot}/var/cache/diald
mknod -m0660 %{buildroot}/var/cache/diald/diald.ctl p

# for diald config

mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
cat > %{buildroot}%{_sysconfdir}/modprobe.d/%{name}.conf << EOF
alias tap0 ethertap
options tap0 -o tap0 unit=0
EOF

# Fix permissions
find %{buildroot} -perm 0744 -exec chmod 0644 '{}' \;

%post
%_post_service diald

%preun
%_preun_service diald

%files
%doc BUGS CHANGES LICENSE NOTES README*
%doc THANKS TODO TODO.budget doc/diald-faq.txt setup contrib
%{_initrddir}/diald
%config(noreplace) %{_sysconfdir}/pam.d/*
%dir %{_sysconfdir}/diald
%config(noreplace) %{_sysconfdir}/diald/*
%config(noreplace) %{_sysconfdir}/modprobe.d/%{name}.conf
%{_bindir}/*
%dir %{_libdir}/diald
%{_libdir}/diald/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*
%dir %{_var}/cache/diald
%attr(660,root,root) %{_var}/cache/diald/diald.ctl


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-15mdv2011.0
+ Revision: 663772
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-14mdv2011.0
+ Revision: 604788
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-13mdv2010.1
+ Revision: 520075
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-12mdv2010.0
+ Revision: 413353
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2009.1
+ Revision: 316554
- rediffed one fuzzy patch

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-10mdv2009.0
+ Revision: 220623
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0-9mdv2008.1
+ Revision: 149179
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 22 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-8mdv2008.0
+ Revision: 42833
- bunzip patches; lsb compliant initscript; use modprobe.d instead of echoing to modules.conf (it's not 1999 any more); rebuild for 2008
- Import diald



* Wed Jun 07 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.0-7mdv2007.0
- fix build with new glibc (P5)
- fix requires for post & preun
- cleanups
- %%mkrel
- fix summary-ended-with-dot
- fix executable-marked-as-config-file

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.0-6mdk
- Rebuild

* Wed Feb 25 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.0-5mdk
- rebuild

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0-4mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT in %%install, not %%prep
- prereq on rpm-helper

* Fri Jan 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.0-3mdk
- rebuild

* Fri Jan 25 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0-2mdk
- bzip2 patch & remove unused ones
- fix post message that gaves warning
- fix directory permission

* Wed Oct 03 2001 Philippe Libat <philippe@mandrakesoft.com> 1.0-1mdk
- new version
- add contrib, setup
- add config file
- fix ethertap modules

* Mon Jul 02 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.99.4-3mdk
- rebuild
- url

* Wed Mar 28 2001 Florin Grad <florin@mandrakesoft.com> 0.99.4-2mdk 
- add the pam file

* Wed Mar 28 2001 Florin Grad <florin@mandrakesoft.com> 0.99.4-1mdk 
- 0.99.4-1mdk
- update the Makefile patch and add the -p0 option
- comment out patch 1 and 2

* Tue Jan 09 2001  Lenny Cartier <lenny@mandrakesoft.com> 0.99.1-5mdk 
- rebuild

* Thu Aug 31 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.99.1-4mdk
- rebuild to fix the init script.
- add a line to description reminding people to have slip in their kernel.
- fix automated build.

* Tue Aug 29 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.99.1-3mdk
- BM

* Wed Apr 26 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.99.1-2mdk
- fix group
- fix files section

* Thu Feb 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.99.1-1mdk
- mandrake build
- modified Makefile-patch file for proper owner during install
