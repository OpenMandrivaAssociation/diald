Summary:	Daemon that provides on demand IP links via SLIP or PPP
Name:		diald
Version:	1.0
Release:	19
License:	GPLv2
Group:		Networking/Other
Url:		http://diald.sourceforge.net
Source0:	%{name}-%{version}.tar.bz2
Source1:	diald.init
Source2:	diald.conf
Source3:	diald.filter
Patch3:		diald-c-files.patch
Patch4:		diald-1.0.patch
Patch5:		diald-1.0-fix-glibc2.4.patch
Requires:	ppp
Requires(post,preun):	rpm-helper

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
%apply_patches

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

