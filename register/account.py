import ldap
import base64
import hashlib
import smtplib
import random
import codecs

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

def create(uid,cn,sn):
  l = ldapsetup()

  if exists(uid):
    return

  uidNumber = random.randint(2000000,5000000)

  while l.search_ext_s(ldapbase, filterstr='(uidNumber=%s)' % uidNumber, scope=ldap.SCOPE_SUBTREE):
      uidNumber = random.randint(2000000,5000000)

  l.add_s('uid=%s,ou=Clients,ou=Users,dc=bils,dc=se' % uid,
             [('homeDirectory', ['/home/%s' % str(uid)]),
              ('sn', [codecs.utf_8_encode(sn)[0]]),
              ('cn', [codecs.utf_8_encode(cn)[0]]),
              ('uid',[str(uid)]),
              ('mail',[str(uid)]),
              ('loginShell', ['/bin/bash']),
              ('objectClass', ['posixAccount', 'shadowAccount', 'inetOrgPerson', 'person', 'top', 'organizationalPerson']),
              ('uidNumber', [str(uidNumber)]),
              ('gidNumber', [str(uidNumber)]),
              ])

def grantservice(uid, servicedn):
  
  l = ldapsetup()
  try:
    l.modify_s(servicedn, ((ldap.MOD_ADD, "memberUid", str(uid)),))
  except ldap.TYPE_OR_VALUE_EXISTS, e:
    pass

def hasservice(uid, servicedn):
  
  l = ldapsetup()

  posts = l.search_ext_s(servicedn, filterstr='(memberUid=%s)' % str(uid), scope=ldap.SCOPE_BASE)

  if posts:
     return True
  return False


f=open('/etc/bilsldap')

ldapuser = f.readline().strip()
ldappass = f.readline().strip()
ldapuri = f.readline().strip()
ldapbase = f.readline().strip()
f.close()


