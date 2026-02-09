
import unittest
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from query_workflow import query_workflow, list_workflows

class TestQueryWorkflow(unittest.TestCase):
    def test_list_includes_capability_group(self):
        """Test that listing workflows includes the capability_group field"""
        result = list_workflows()
        self.assertIn('categories', result)
        
        # Check a known workflow if core category exists
        core_category = result['categories'].get('core', [])
        if core_category:
            first_workflow = core_category[0]
            self.assertIn('capability_group', first_workflow)

    def test_query_includes_capability_group(self):
        """Test that querying a specific workflow includes capability_group"""
        # We assume 'plan' or 'skt:plan' exists as it is core
        result = query_workflow('plan')
        if 'error' not in result:
            workflow = result['workflow']
            self.assertIn('capability_group', workflow)
            self.assertEqual(workflow['capability_group'], 'essential')
        else:
            # Try skt:plan
            result = query_workflow('skt:plan')
            if 'error' not in result:
                workflow = result['workflow']
                self.assertIn('capability_group', workflow)
                self.assertEqual(workflow['capability_group'], 'essential')

if __name__ == '__main__':
    unittest.main()
