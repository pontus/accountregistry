import ldap
import base64
import hashlib
import smtplib

ldapConnection = None

def ldapsetup():
  global ldapConnection

  if ldapConnection:
      return ldapConnection

  ldapConnection = ldap.initialize(ldapuri)
  ldapConnection.set_option(ldap.OPT_X_TLS_CACERTDIR, "/etc/openldap/cacerts")
  ldapConnection.start_tls_s()
  ldapConnection.simple_bind_s(ldapuser, ldappass)
  return ldapConnection


def exists(s):
    l = ldapsetup()

    posts = l.search_ext_s(ldapbase, filterstr='(uid=%s)' % s, scope=ldap.SCOPE_SUBTREE)       
    
    if posts:
        return True
    return False

def changepwd(uid, newpwd):
    l = ldapsetup()
    data = l.search_ext_s(ldapbase, filterstr='(uid=%s)' % uid, scope=ldap.SCOPE_SUBTREE)       

    if len(data) != 1:
        raise Exception("Something wrong")

    dn = data[0][0]

    # LDAP is set up to automatically fix MD5 encoding
    l.modify_s(dn, ((ldap.MOD_REPLACE, "userPassword", newpwd),))



f=open('/etc/bilsldap')

ldapuser = f.readline().strip()
ldappass = f.readline().strip()
ldapuri = f.readline().strip()
ldapbase = f.readline().strip()
f.close()


