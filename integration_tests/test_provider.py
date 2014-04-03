from integration_tests.base import BaseTestCase


class ProviderClassTest(BaseTestCase):
    cloud_account = lambda self, identity: {"name": "dummy_default", "provider": "aws-ec2", "usedEnvironments": [],
                                            "ec2SecurityGroup": "default", "providerCopy": "aws-ec2",
                                            "jcloudsIdentity": identity, "jcloudsCredential": "secret",
                                            "jcloudsRegions": "us-east-1"}

    def test_provider_crud(self):
        # create
        provider = self.organization.create_provider(name='crud', parameters=self.cloud_account('abc'))
        identity = lambda: [p['value'] for p in provider.json()['params'] if p['param']['param']['name'] == 'jcloudsIdentity'][0]
        assert provider in self.organization.providers
        assert provider.name == 'crud'
        assert identity() == 'abc'

        #read
        assert self.organization.get_provider(id=provider.id) == provider
        assert self.organization.get_provider(name=provider.name) == provider
        assert self.organization.get_or_create_provider(provider.name) == provider

        #update
        provider.update('crud_updated', self.cloud_account('abc_updated'))

        assert provider.name == 'crud_updated'
        assert identity() == 'abc_updated'

        provider.update(parameters=self.cloud_account('abc_updated_twice'))
        assert provider.name == 'dummy_default'
        assert identity() == 'abc_updated_twice'

        assert self.organization.provider(name='dummy_default', parameters=self.cloud_account('abc_set')) == provider
        assert identity() == 'abc_set'

        #delete
        id = provider.id
        provider.delete()
        assert id not in self.organization.providers