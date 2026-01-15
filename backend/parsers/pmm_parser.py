import pandas as pd
from datetime import datetime

class PMMParser:
    """Parse PMM Excel/CSV files and map to output schema"""

    COLUMN_MAPPING = {
        'Customer Need': 'Customer need',
        'Need Description': 'Need description',
        'Request Type': 'Request type',
        'Customer Persona(s)': 'Personas',
        'Customer Sales Segment(s)': 'Sales Segment',
        'Listening Type(s)': 'Listening Type',
        '# of Customers Supporting': '# of customers',
        'PMM Aligned': 'PMM',
        'Product PM': 'PM',
        'Date Added (mm/dd/yy)': 'Date Created (mm/dd/yy)'
    }

    VALUE_TRANSLATIONS = {
        'Customer Reach': {
            'Extremely High (51%+)': 'XXL',
            'High (26-50%)': 'L',
            'Medium (11-25%)': 'M',
            'Low (1-10%)': 'S'
        },
        'Annual Revenue Increase': {
            'Low (+$1M-$100M)': 'S',
            'Medium (+$101M-$500M)': 'M',
            'High (+$501M-$1B)': 'L'
        },
        'Status': {
            'Live': 'Launched',
            'In Development': 'In Development',
            'On Roadmap - Current Cycle': 'Roadmap - Current Cycle',
            'On Roadmap - Future Cycle': 'Backlog',
            'Validating/Sizing (BRD)': 'Validating/Sizing',
            'Discovery': 'Discovery',
            'Unknown': 'Not Evaluated',
            'Previously Rejected': 'Declined'
        }
    }

    def parse(self, file_path):
        """Parse PMM file and return structured data"""
        df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)

        items = []
        for idx, row in df.iterrows():
            item = {
                'source_type': 'PMM',
                'source_row_num': idx + 2,  # Excel row number
                'unique_id': f"PMM_{idx + 1:03d}",
                'listening_source': 'PMM',
                'last_updated': datetime.now().strftime('%m/%d/%y')
            }

            # Direct mappings
            for source_col, target_col in self.COLUMN_MAPPING.items():
                if source_col in df.columns:
                    item[target_col] = row[source_col]

            # Value translations
            if 'Customer Reach' in df.columns:
                reach_val = str(row['Customer Reach'])
                item['Reach [T-Shirt Size]'] = self.VALUE_TRANSLATIONS['Customer Reach'].get(reach_val, '')

            if 'Annual Revenue Increase' in df.columns:
                rev_val = str(row['Annual Revenue Increase'])
                item['Revenue [Tshirt Size]'] = self.VALUE_TRANSLATIONS['Annual Revenue Increase'].get(rev_val, '')

            if 'Status' in df.columns:
                status_val = str(row['Status'])
                item['Roadmap Status'] = self.VALUE_TRANSLATIONS['Status'].get(status_val, 'Not Evaluated')

            # Fields for LLM to generate/refine
            item['needs_llm_categorization'] = True
            item['llm_context'] = {
                'pmm_product_area': row.get('Product/Feature Area', ''),
                'pmm_product_feature': row.get('Product/Feature', ''),
                'pmm_need_granularity': row.get('Need Level of Granularity', '')
            }

            # Auto-populate defaults
            item['Rev Blocker [Flag]'] = 'No'
            item['CX Insights Priority Needs (y/n)'] = 'No'
            item['Growth Blocker List (y/n)'] = 'No'

            items.append(item)

        return items
