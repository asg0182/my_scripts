import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.common.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.jenkins.plugins.sshcredentials.impl.*
import hudson.plugins.sshslaves.*;

global_domain = Domain.global()
  credentials_store =
  Jenkins.instance.getExtensionList(
           'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
         )[0].getStore()

def create_credentials(String username, String user_private_key, String description, String cr_id){
  private_key = user_private_key
  credentials = new BasicSSHUserPrivateKey(
        CredentialsScope.GLOBAL,
        cr_id,
        username,
        new BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(private_key),
        "",
        description
        )
credentials_store.addCredentials(global_domain, credentials)
return "credential add for "+username
}
def create_credentials_with_password(String username, String password, String description, String cr_id){
credentials = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        cr_id,
        description,
        username,
        password
      )
credentials_store.addCredentials(global_domain, credentials)
return "credential add for "+username
}
println create_credentials('jenkins', """-----BEGIN RSA PRIVATE KEY-----
private ssh key ...
-----END RSA PRIVATE KEY-----""", 'jenkins-git', 'jenkins-git')
println create_credentials_with_password('dockeradm','example', 'jenkins-ansible', 'jenkins-ansible')
println create_credentials_with_password('jenkins','example', 'jenkins-http', 'jenkins-http')
