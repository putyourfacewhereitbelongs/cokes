const XLSX = require('xlsx');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('public/data/drinks.json', 'utf8'));

const wb = XLSX.utils.book_new();

// Sheet 1: Master Inventory (All 276 Ready-to-Drink Products)
const masterRows = data.map((d, i) => ({
  'Row #': i + 1,
  'myCoke SKU': d.sku,
  'UPC Barcode': d.upc || '',
  'Beverage Full Name': d.full_name,
  'Brand Group': d.brand_group,
  'Category': d.category,
  'Size': d.size,
  'Container Type': d.container_type,
  'Packaging / Pack Count': d.packaging,
  'Cooler Door / Planogram Zone': d.cooler_zone || '',
  'Photo File': d.image_path
}));

const wsMaster = XLSX.utils.json_to_sheet(masterRows);
wsMaster['!cols'] = [
  { wch: 8 },  // Row #
  { wch: 14 }, // SKU
  { wch: 16 }, // UPC
  { wch: 45 }, // Full Name
  { wch: 25 }, // Brand Group
  { wch: 26 }, // Category
  { wch: 12 }, // Size
  { wch: 16 }, // Container
  { wch: 22 }, // Packaging
  { wch: 40 }, // Cooler Door
  { wch: 25 }  // Photo
];

XLSX.utils.book_append_sheet(wb, wsMaster, "Master Beverages (276)");

// Category Sheets
const sheets = [
  { name: 'Colas & Soft Drinks', filter: d => d.category === 'Carbonated Soft Drinks' },
  { name: 'Energy Drinks', filter: d => d.category === 'Energy Drinks' },
  { name: 'Sports & Hydration', filter: d => d.category === 'Sports & Hydration' },
  { name: 'Waters & Wellness', filter: d => ['Bottled & Enhanced Water', 'Enhanced Water & Wellness', 'Sparkling Water & Seltzers'].includes(d.category) },
  { name: 'Juices & Teas', filter: d => ['Juices & Fruit Drinks', 'Ready-to-Drink Teas', 'Kids Drinks & Juices'].includes(d.category) },
  { name: 'Dairy & Coffee', filter: d => ['Dairy & Protein Drinks', 'Ready-to-Drink Coffee'].includes(d.category) }
];

sheets.forEach(s => {
  const filtered = data.filter(s.filter);
  const rows = filtered.map((d, i) => ({
    'Row #': i + 1,
    'myCoke SKU': d.sku,
    'UPC Barcode': d.upc || '',
    'Beverage Full Name': d.full_name,
    'Brand Group': d.brand_group,
    'Size': d.size,
    'Container': d.container_type,
    'Packaging': d.packaging,
    'Cooler Door / Zone': d.cooler_zone || ''
  }));
  const ws = XLSX.utils.json_to_sheet(rows);
  ws['!cols'] = [
    { wch: 8 }, { wch: 14 }, { wch: 16 }, { wch: 45 }, { wch: 25 }, { wch: 12 }, { wch: 16 }, { wch: 22 }, { wch: 40 }
  ];
  XLSX.utils.book_append_sheet(wb, ws, s.name);
});

XLSX.writeFile(wb, 'Harrys_Beverage_Catalog_Master.xlsx');
console.log('Successfully regenerated Harrys_Beverage_Catalog_Master.xlsx with 276 ready-to-drink beverages!');
