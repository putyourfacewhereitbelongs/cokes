/**
 * HARRY'S CONVENIENCE STORES - READY-TO-DRINK BEVERAGE TRAINING SYSTEM
 * Professional Excel Table Engine + Ultra-Compact Multi-Column Training Reference Sheet
 * 276 Ready-to-Drink Bottled & Canned Beverages
 */

(function () {
  'use strict';

  // State Management
  const state = {
    drinks: [],
    defaultDrinks: [],
    filteredDrinks: [],
    currentSheet: 'ALL', // 'ALL', 'CSD', 'ENERGY', 'SPORTS', 'WATER', 'JUICE', 'DAIRY'
    currentBrandFilter: 'ALL',
    searchQuery: '',
    sortField: 'row_num',
    sortDirection: 'asc',
    selectedRowId: null,
    selectedRowIds: new Set(),
    editingCellInfo: null, // { id, field }
    
    // View mode: 'excel' or 'training'
    viewMode: 'excel',
    trainingDensity: '3-col', // '3-col', '4-col', '2-col'
    trainingDepartment: 'ALL'
  };

  // 6 Structured Departments Config
  const DEPARTMENT_CONFIG = [
    {
      id: 'CSD',
      title: '🥤 1. Colas & Carbonated Soft Drinks',
      shortName: 'Colas & Soft Drinks',
      category: 'Carbonated Soft Drinks'
    },
    {
      id: 'ENERGY',
      title: '⚡ 2. Energy Drinks',
      shortName: 'Energy Drinks',
      category: 'Energy Drinks'
    },
    {
      id: 'SPORTS',
      title: '🏃 3. Sports & Hydration',
      shortName: 'Sports & Hydration',
      category: 'Sports & Hydration'
    },
    {
      id: 'WATER',
      title: '💧 4. Waters & Wellness',
      shortName: 'Waters & Wellness',
      category: ['Bottled & Enhanced Water', 'Enhanced Water & Wellness', 'Sparkling Water & Seltzers']
    },
    {
      id: 'JUICE',
      title: '🧃 5. Juices, Teas & Kids Drinks',
      shortName: 'Juices, Teas & Kids',
      category: ['Juices & Fruit Drinks', 'Ready-to-Drink Teas', 'Kids Drinks & Juices']
    },
    {
      id: 'DAIRY',
      title: '🥛 6. Dairy, Coffee & Protein',
      shortName: 'Dairy, Coffee & Protein',
      category: ['Dairy & Protein Drinks', 'Ready-to-Drink Coffee']
    }
  ];

  // Sheet definitions matching categories
  const SHEET_CONFIG = [
    { id: 'ALL', name: '📊 Master Catalog (All 276)', category: 'ALL' },
    { id: 'CSD', name: '🥤 Colas & Soft Drinks (85)', category: 'Carbonated Soft Drinks' },
    { id: 'ENERGY', name: '⚡ Energy Drinks (83)', category: 'Energy Drinks' },
    { id: 'SPORTS', name: '🏃 Sports & Hydration (40)', category: 'Sports & Hydration' },
    { id: 'WATER', name: '💧 Waters & Wellness (27)', category: ['Bottled & Enhanced Water', 'Enhanced Water & Wellness', 'Sparkling Water & Seltzers'] },
    { id: 'JUICE', name: '🧃 Juices, Teas & Kids (26)', category: ['Juices & Fruit Drinks', 'Ready-to-Drink Teas', 'Kids Drinks & Juices'] },
    { id: 'DAIRY', name: '🥛 Dairy, Coffee & Protein (15)', category: ['Dairy & Protein Drinks', 'Ready-to-Drink Coffee'] }
  ];

  // DOM Elements
  const el = {
    // View Switcher
    viewModeExcelBtn: document.getElementById('view-mode-excel-btn'),
    viewModeTrainingBtn: document.getElementById('view-mode-training-btn'),
    headerSkuBadge: document.getElementById('header-sku-badge'),

    // Excel View Components
    excelRibbonBar: document.getElementById('excel-ribbon-bar'),
    excelFormulaBar: document.getElementById('excel-formula-bar'),
    excelSheetsBar: document.getElementById('excel-sheets-bar'),
    excelGridViewport: document.getElementById('excel-grid-viewport'),
    excelStatusBar: document.getElementById('excel-status-bar'),
    
    // Sheet tabs & Pills
    sheetsContainer: document.getElementById('excel-sheets-bar'),
    formulaPillsContainer: document.getElementById('formula-pills-bar'),
    
    // Search & Filter
    searchInput: document.getElementById('excel-search-input'),
    searchClearBtn: document.getElementById('excel-search-clear'),
    
    // Table Grid
    tableBody: document.getElementById('excel-table-body'),
    tableHeaders: document.querySelectorAll('.excel-data-header-row th.sortable'),
    
    // Status Bar
    statusRowCount: document.getElementById('status-row-count'),
    statusFilteredCount: document.getElementById('status-filtered-count'),
    statusSheetName: document.getElementById('status-sheet-name'),
    statusSelectedCount: document.getElementById('status-selected-count'),
    
    // Ribbon Buttons
    addRowBtn: document.getElementById('ribbon-add-row-btn'),
    deleteRowBtn: document.getElementById('ribbon-delete-row-btn'),
    duplicateRowBtn: document.getElementById('ribbon-duplicate-row-btn'),
    exportXlsxBtn: document.getElementById('ribbon-export-xlsx-btn'),
    exportCsvBtn: document.getElementById('ribbon-export-csv-btn'),
    importFileBtn: document.getElementById('ribbon-import-file-btn'),
    fileInput: document.getElementById('excel-file-input'),
    printSheetBtn: document.getElementById('ribbon-print-sheet-btn'),
    resetCatalogBtn: document.getElementById('ribbon-reset-catalog-btn'),
    trainingGuideBtn: document.getElementById('ribbon-training-guide-btn'),
    
    // Training Sheet View
    trainingSheetViewport: document.getElementById('training-sheet-viewport'),
    trainSectionsContainer: document.getElementById('train-sections-container'),
    trainPrintNowBtn: document.getElementById('train-print-now-btn'),
    trainDensitySelect: document.getElementById('train-density-select'),
    trainDepartmentSelect: document.getElementById('train-department-select'),
    trainReturnExcelBtn: document.getElementById('train-return-excel-btn'),
    trainPrintDate: document.getElementById('train-print-date'),

    // Modals
    drinkModal: document.getElementById('drink-modal'),
    drinkForm: document.getElementById('drink-form'),
    drinkModalTitle: document.getElementById('drink-modal-title'),
    zoomModal: document.getElementById('zoom-modal'),
    zoomModalImg: document.getElementById('zoom-modal-img'),
    zoomModalTitle: document.getElementById('zoom-modal-title'),
    zoomModalSub: document.getElementById('zoom-modal-sub'),
    trainingModal: document.getElementById('training-modal'),
    
    toastContainer: document.getElementById('toast-container')
  };

  // Initialize Application
  async function init() {
    try {
      const response = await fetch('data/drinks.json');
      const data = await response.json();
      state.defaultDrinks = JSON.parse(JSON.stringify(data));
      
      const saved = localStorage.getItem('harrys_drinks_rtd_master_v3');
      if (saved) {
        try {
          state.drinks = JSON.parse(saved);
        } catch (e) {
          state.drinks = JSON.parse(JSON.stringify(state.defaultDrinks));
        }
      } else {
        state.drinks = JSON.parse(JSON.stringify(state.defaultDrinks));
      }
      
      // Update print date
      if (el.trainPrintDate) {
        const today = new Date();
        el.trainPrintDate.innerHTML = `<strong>Date:</strong> ${today.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
      }

      renderSheetTabs();
      renderFormulaPills();
      setupEvents();
      filterAndRenderTable();
      renderTrainingSheet();
      updateStatusBar();
      
    } catch (err) {
      console.error('Initialization error:', err);
      showToast('Error loading drink catalog data', 'error');
    }
  }

  // Save State to LocalStorage
  function saveState() {
    try {
      localStorage.setItem('harrys_drinks_rtd_master_v3', JSON.stringify(state.drinks));
    } catch (e) {
      console.error('Failed to save to localStorage:', e);
    }
    updateStatusBar();
    renderTrainingSheet();
  }

  // Switch View Modes: Excel vs Training Guide
  function setViewMode(mode) {
    state.viewMode = mode;
    if (mode === 'training') {
      document.body.classList.remove('view-excel');
      document.body.classList.add('view-training');
      el.viewModeExcelBtn.classList.remove('active');
      el.viewModeTrainingBtn.classList.add('active');
      renderTrainingSheet();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      document.body.classList.remove('view-training');
      document.body.classList.add('view-excel');
      el.viewModeTrainingBtn.classList.remove('active');
      el.viewModeExcelBtn.classList.add('active');
      filterAndRenderTable();
    }
  }

  // Render Excel Sheet Tabs
  function renderSheetTabs() {
    let html = '';
    
    SHEET_CONFIG.forEach(sheet => {
      let count = 0;
      if (sheet.category === 'ALL') {
        count = state.drinks.length;
      } else if (Array.isArray(sheet.category)) {
        count = state.drinks.filter(d => sheet.category.includes(d.category)).length;
      } else {
        count = state.drinks.filter(d => d.category === sheet.category).length;
      }
      
      const isActive = state.currentSheet === sheet.id;
      const cleanName = sheet.name.replace(/\s\(\d+\)$/, '');
      html += `
        <div class="excel-sheet-tab ${isActive ? 'active' : ''}" data-sheet-id="${sheet.id}">
          <span>${cleanName}</span>
          <span class="excel-sheet-count">${count}</span>
        </div>
      `;
    });
    
    el.sheetsContainer.innerHTML = html;
  }

  // Render Brand Quick Filter Pills in Formula Bar
  function renderFormulaPills() {
    const priorityPills = [
      { label: 'All Brands', value: 'ALL' },
      { label: 'Coke with Coke', value: 'Coca-Cola' },
      { label: 'Diet Coke', value: 'Diet Coke' },
      { label: 'Sprite', value: 'Sprite' },
      { label: 'Dr Pepper', value: 'Dr Pepper' },
      { label: 'Fanta', value: 'Fanta' },
      { label: 'Monster Ultra', value: 'Monster Energy Ultra' },
      { label: 'Monster Juice', value: 'Monster Energy Juice' },
      { label: 'Monster Core', value: 'Monster Energy' },
      { label: 'Reign Energy', value: 'Reign Total Body Fuel' },
      { label: 'Bang Energy', value: 'Bang Energy' },
      { label: 'NOS Energy', value: 'NOS Energy' },
      { label: 'BODYARMOR', value: 'BODYARMOR SuperDrink & Lyte' },
      { label: 'Flash I.V.', value: 'BODYARMOR Flash I.V.' },
      { label: 'Powerade', value: 'Powerade' },
      { label: 'smartwater', value: 'smartwater' },
      { label: 'vitaminwater', value: 'vitaminwater' },
      { label: 'Minute Maid', value: 'Minute Maid' },
      { label: 'Gold Peak Tea', value: 'Gold Peak Tea' },
      { label: 'Core Power 42g/26g', value: 'Core Power Protein' },
      { label: 'Fairlife Milk', value: 'Fairlife Milk' },
      { label: "Dunkin' Coffee", value: "Dunkin' Iced Coffee" }
    ];
    
    let html = `<span style="font-weight: 700; color: #6B7280; font-size: 11px; margin-right: 4px;">Quick Brand Filter:</span>`;
    priorityPills.forEach(p => {
      const active = state.currentBrandFilter === p.value ? 'active' : '';
      html += `<button type="button" class="excel-filter-pill ${active}" data-brand-filter="${p.value}">${p.label}</button>`;
    });
    
    el.formulaPillsContainer.innerHTML = html;
  }

  // Filter & Render Table Rows
  function filterAndRenderTable() {
    const q = state.searchQuery.toLowerCase().trim();
    const sheetCfg = SHEET_CONFIG.find(s => s.id === state.currentSheet) || SHEET_CONFIG[0];
    
    state.filteredDrinks = state.drinks.filter(d => {
      // Sheet Category Filter
      if (sheetCfg.category !== 'ALL') {
        if (Array.isArray(sheetCfg.category)) {
          if (!sheetCfg.category.includes(d.category)) return false;
        } else {
          if (d.category !== sheetCfg.category) return false;
        }
      }
      
      // Brand Filter Pill
      if (state.currentBrandFilter !== 'ALL') {
        if (d.brand_group !== state.currentBrandFilter) return false;
      }
      
      // Search Text
      if (q) {
        const matchName = (d.full_name || '').toLowerCase().includes(q);
        const matchBrand = (d.brand_group || '').toLowerCase().includes(q);
        const matchCat = (d.category || '').toLowerCase().includes(q);
        const matchSku = (d.sku || '').toLowerCase().includes(q);
        const matchUpc = (d.upc || '').toLowerCase().includes(q);
        const matchSize = (d.size || '').toLowerCase().includes(q);
        const matchPack = (d.packaging || '').toLowerCase().includes(q);
        const matchDoor = (d.cooler_zone || '').toLowerCase().includes(q);
        
        if (!matchName && !matchBrand && !matchCat && !matchSku && !matchUpc && !matchSize && !matchPack && !matchDoor) {
          return false;
        }
      }
      
      return true;
    });
    
    // Sort
    const f = state.sortField;
    const dir = state.sortDirection === 'asc' ? 1 : -1;
    
    state.filteredDrinks.sort((a, b) => {
      let valA = a[f] ?? '';
      let valB = b[f] ?? '';
      
      if (f === 'row_num') {
        return dir * ((a.row_num || 0) - (b.row_num || 0));
      }
      if (f === 'size') {
        return dir * String(valA).localeCompare(String(valB), undefined, { numeric: true });
      }
      return dir * String(valA).localeCompare(String(valB));
    });
    
    renderTableRows();
    updateSortHeaderClasses();
    updateStatusBar();
  }

  // Render Table Rows with Section Sub-Headers
  function renderTableRows() {
    if (state.filteredDrinks.length === 0) {
      el.tableBody.innerHTML = `
        <tr>
          <td colspan="12" style="text-align: center; padding: 40px; color: #6B7280; background: #FFFFFF;">
            <div style="font-size: 24px; margin-bottom: 6px;">🔍</div>
            <div style="font-weight: 700; font-size: 13px; color: #111827;">No matching beverages found</div>
            <div style="font-size: 11px; margin-top: 4px;">Try clearing search keywords or switching sheet tabs.</div>
            <button type="button" class="excel-btn excel-btn-primary" style="margin-top: 10px;" onclick="window.HarrysExcel.clearFilters()">Clear All Filters</button>
          </td>
        </tr>
      `;
      return;
    }
    
    let html = '';
    let lastBrandGroup = null;
    
    state.filteredDrinks.forEach((drink, idx) => {
      const isSelected = state.selectedRowId === drink.id || state.selectedRowIds.has(drink.id);
      
      // If we are in "All Inventory" view or sorting by category/brand, insert clean Section Headers
      if (state.sortField === 'row_num' || state.sortField === 'category' || state.sortField === 'brand_group') {
        if (drink.brand_group !== lastBrandGroup) {
          lastBrandGroup = drink.brand_group;
          
          let brandBadgeClass = 'excel-brand-group-badge';
          if (drink.brand_group.includes('Coca-Cola') || drink.brand_group.includes('Diet Coke')) brandBadgeClass += ' coke';
          else if (drink.brand_group.includes('Monster') || drink.brand_group.includes('Reign')) brandBadgeClass += ' monster';
          else if (drink.brand_group.includes('Powerade') || drink.brand_group.includes('BODYARMOR')) brandBadgeClass += ' sports';
          
          html += `
            <tr class="excel-section-row no-select">
              <td class="excel-row-header-cell">▶</td>
              <td colspan="11">
                <strong>${escapeHtml(drink.brand_group)} Family</strong>
                <span style="font-size: 10px; color: #64748B; font-weight: 500; margin-left: 8px;">• ${escapeHtml(drink.category)}</span>
              </td>
            </tr>
          `;
        }
      }
      
      html += `
        <tr class="excel-data-row ${isSelected ? 'is-selected' : ''}" data-id="${drink.id}" data-row="${idx + 1}">
          <!-- Row Number Column -->
          <td class="excel-row-header-cell">${idx + 1}</td>
          
          <!-- Column A: Tiny Drink Photo (Click to Zoom) -->
          <td class="excel-img-cell" title="Click to enlarge drink photo">
            <div class="excel-drink-thumb-box" onclick="window.HarrysExcel.openZoom('${drink.id}')">
              <img src="${drink.image_path}" alt="${escapeHtml(drink.full_name)}" class="excel-drink-thumb-img" loading="lazy" onerror="this.src='harrys-h-emblem.svg'">
            </div>
          </td>
          
          <!-- Column B: Full Beverage Name (Editable) -->
          <td class="excel-editable-cell excel-drink-name-cell" data-field="full_name" style="width: 260px;" title="Double-click to edit name">
            <strong>${escapeHtml(drink.full_name)}</strong>
          </td>
          
          <!-- Column C: Brand Group (Editable) -->
          <td class="excel-editable-cell" data-field="brand_group" style="width: 140px;" title="Double-click to edit brand">
            <span class="excel-brand-group-badge">${escapeHtml(drink.brand_group)}</span>
          </td>
          
          <!-- Column D: Drink Category (Editable) -->
          <td class="excel-editable-cell" data-field="category" style="width: 150px; color: #4B5563;" title="Double-click to edit category">
            ${escapeHtml(drink.category)}
          </td>
          
          <!-- Column E: Size (Editable) -->
          <td class="excel-editable-cell" data-field="size" style="width: 80px; font-weight: 700; color: #111827;" title="Double-click to edit size">
            ${escapeHtml(drink.size)}
          </td>
          
          <!-- Column F: Container Type (Editable) -->
          <td class="excel-editable-cell" data-field="container_type" style="width: 100px; color: #4B5563;" title="Double-click to edit container">
            ${escapeHtml(drink.container_type)}
          </td>
          
          <!-- Column G: Packaging / Case Count (Editable) -->
          <td class="excel-editable-cell" data-field="packaging" style="width: 110px; color: #374151;" title="Double-click to edit packaging">
            ${escapeHtml(drink.packaging)}
          </td>
          
          <!-- Column H: myCoke SKU # (Editable) -->
          <td class="excel-editable-cell excel-mono-text" data-field="sku" style="width: 90px;" title="Double-click to edit SKU">
            <span class="excel-sku-tag">#${escapeHtml(drink.sku)}</span>
          </td>
          
          <!-- Column I: UPC Barcode (Editable) -->
          <td class="excel-editable-cell excel-mono-text" data-field="upc" style="width: 120px; color: #4B5563;" title="Double-click to edit UPC">
            ${escapeHtml(drink.upc || '-')}
          </td>
          
          <!-- Column J: Cooler Door / Zone (Editable) -->
          <td class="excel-editable-cell" data-field="cooler_zone" style="width: 190px; color: #4B5563; font-size: 11px;" title="Double-click to edit zone">
            ${escapeHtml(drink.cooler_zone || '-')}
          </td>
          
          <!-- Column K: Actions -->
          <td class="excel-action-col no-print" style="width: 75px; text-align: center;">
            <button type="button" class="excel-btn" style="padding: 2px 6px; font-size: 11px;" onclick="window.HarrysExcel.openEditModal('${drink.id}')" title="Edit Full Details">
              ✏️
            </button>
            <button type="button" class="excel-btn" style="padding: 2px 6px; font-size: 11px; color: var(--harrys-red);" onclick="window.HarrysExcel.deleteRow('${drink.id}')" title="Delete Row">
              🗑️
            </button>
          </td>
        </tr>
      `;
    });
    
    el.tableBody.innerHTML = html;
  }

  // RENDER ULTRA-COMPACT PRINTABLE TRAINING SHEET (3/4-Column Pocket Reference Guide)
  function renderTrainingSheet() {
    const selectedDept = state.trainingDepartment || 'ALL';
    const density = state.trainingDensity || '3-col';
    
    let html = '';
    
    DEPARTMENT_CONFIG.forEach(dept => {
      if (selectedDept !== 'ALL' && dept.id !== selectedDept) {
        return;
      }
      
      let deptDrinks = [];
      if (Array.isArray(dept.category)) {
        deptDrinks = state.drinks.filter(d => dept.category.includes(d.category));
      } else {
        deptDrinks = state.drinks.filter(d => d.category === dept.category);
      }
      
      if (deptDrinks.length === 0) return;
      
      html += `
        <div class="train-category-section" data-dept="${dept.id}">
          <div class="train-category-header">
            <span class="train-cat-title">${dept.title}</span>
            <span class="train-cat-badge">${deptDrinks.length} SKUs</span>
          </div>
          <div class="train-items-grid cols-${density.replace('-col', '')}">
      `;
      
      deptDrinks.forEach(drink => {
        html += `
          <div class="train-item" data-id="${drink.id}" onclick="window.HarrysExcel.openZoom('${drink.id}')" title="Click to preview drink bottle/can">
            <div class="train-item-img-box">
              <img src="${drink.image_path}" alt="${escapeHtml(drink.full_name)}" class="train-item-img" loading="lazy" onerror="this.src='harrys-h-emblem.svg'">
            </div>
            <div class="train-item-content">
              <div class="train-item-name">${escapeHtml(drink.full_name)}</div>
              <div class="train-item-details">
                <span class="train-item-size">${escapeHtml(drink.size)} ${escapeHtml(drink.container_type.replace('Plastic Bottle', 'Bottle').replace('Aluminum Bottle', 'Alum Bottle'))}</span>
                <span class="train-item-sep">•</span>
                <span>${escapeHtml(drink.packaging)}</span>
                <span class="train-item-sep">•</span>
                <span class="train-item-sku">SKU ${escapeHtml(drink.sku)}</span>
              </div>
            </div>
          </div>
        `;
      });
      
      html += `
          </div>
        </div>
      `;
    });
    
    if (el.trainSectionsContainer) {
      el.trainSectionsContainer.innerHTML = html;
    }
  }

  // Update Status Bar
  function updateStatusBar() {
    const total = state.drinks.length;
    const filtered = state.filteredDrinks.length;
    
    if (el.statusRowCount) el.statusRowCount.textContent = total;
    if (el.statusFilteredCount) el.statusFilteredCount.textContent = filtered;
    if (el.headerSkuBadge) el.headerSkuBadge.textContent = `${total} Ready-to-Drink SKUs`;
    
    const sheetCfg = SHEET_CONFIG.find(s => s.id === state.currentSheet);
    if (el.statusSheetName && sheetCfg) {
      el.statusSheetName.textContent = sheetCfg.name.replace(/\s\(\d+\)$/, '');
    }
    
    if (el.statusSelectedCount) {
      if (state.selectedRowId) {
        const item = state.drinks.find(d => d.id === state.selectedRowId);
        if (item) {
          el.statusSelectedCount.textContent = `Selected: ${item.full_name} (${item.size}) • SKU: #${item.sku}`;
        }
      } else {
        el.statusSelectedCount.textContent = `Ready • ${total} Ready-to-Drink Items`;
      }
    }
  }

  // Update Sort Header Icons
  function updateSortHeaderClasses() {
    el.tableHeaders.forEach(th => {
      const field = th.dataset.sort;
      th.classList.remove('sort-asc', 'sort-desc');
      if (field === state.sortField) {
        th.classList.add(state.sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
      }
    });
  }

  // Setup UI Events
  function setupEvents() {
    // View Switcher Buttons
    if (el.viewModeExcelBtn) {
      el.viewModeExcelBtn.addEventListener('click', () => setViewMode('excel'));
    }
    if (el.viewModeTrainingBtn) {
      el.viewModeTrainingBtn.addEventListener('click', () => setViewMode('training'));
    }

    // Training Sheet Controls
    if (el.trainPrintNowBtn) {
      el.trainPrintNowBtn.addEventListener('click', () => {
        window.print();
      });
    }
    if (el.trainReturnExcelBtn) {
      el.trainReturnExcelBtn.addEventListener('click', () => {
        setViewMode('excel');
      });
    }
    if (el.trainDensitySelect) {
      el.trainDensitySelect.addEventListener('change', (e) => {
        state.trainingDensity = e.target.value;
        renderTrainingSheet();
      });
    }
    if (el.trainDepartmentSelect) {
      el.trainDepartmentSelect.addEventListener('change', (e) => {
        state.trainingDepartment = e.target.value;
        renderTrainingSheet();
      });
    }

    // Sheet Tabs Click
    el.sheetsContainer.addEventListener('click', (e) => {
      const tab = e.target.closest('.excel-sheet-tab');
      if (tab) {
        const sheetId = tab.dataset.sheetId;
        state.currentSheet = sheetId;
        renderSheetTabs();
        filterAndRenderTable();
      }
    });

    // Formula Brand Filter Pills
    el.formulaPillsContainer.addEventListener('click', (e) => {
      const pill = e.target.closest('.excel-filter-pill');
      if (pill) {
        state.currentBrandFilter = pill.dataset.brandFilter;
        renderFormulaPills();
        filterAndRenderTable();
      }
    });

    // Live Search
    let searchTimeout;
    el.searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        state.searchQuery = e.target.value;
        filterAndRenderTable();
      }, 150);
    });

    el.searchClearBtn.addEventListener('click', () => {
      el.searchInput.value = '';
      state.searchQuery = '';
      filterAndRenderTable();
    });

    // Sort Headers
    el.tableHeaders.forEach(th => {
      th.addEventListener('click', () => {
        const field = th.dataset.sort;
        if (state.sortField === field) {
          state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          state.sortField = field;
          state.sortDirection = 'asc';
        }
        filterAndRenderTable();
      });
    });

    // Row Selection Click
    el.tableBody.addEventListener('click', (e) => {
      const row = e.target.closest('.excel-data-row');
      if (!row) return;
      
      const id = row.dataset.id;
      if (state.selectedRowId === id) {
        state.selectedRowId = null;
      } else {
        state.selectedRowId = id;
      }
      
      document.querySelectorAll('.excel-data-row').forEach(r => {
        r.classList.toggle('is-selected', r.dataset.id === state.selectedRowId);
      });
      updateStatusBar();
    });

    // Double-Click Inline Cell Editing
    el.tableBody.addEventListener('dblclick', (e) => {
      const cell = e.target.closest('.excel-editable-cell');
      if (!cell) return;
      
      const row = cell.closest('.excel-data-row');
      const id = row.dataset.id;
      const field = cell.dataset.field;
      const item = state.drinks.find(d => d.id === id);
      if (!item) return;

      const currentVal = item[field] ?? '';
      cell.classList.add('is-editing');
      
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'excel-inline-input';
      input.value = currentVal;
      
      cell.innerHTML = '';
      cell.appendChild(input);
      input.focus();
      input.select();

      function commit() {
        const newVal = input.value.trim();
        item[field] = newVal;
        cell.classList.remove('is-editing');
        saveState();
        filterAndRenderTable();
        showToast(`Updated ${field.replace('_', ' ')}`, 'info');
      }

      input.addEventListener('blur', commit);
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') {
          input.blur();
        } else if (ev.key === 'Escape') {
          cell.classList.remove('is-editing');
          filterAndRenderTable();
        }
      });
    });

    // Ribbon: Insert Row
    el.addRowBtn.addEventListener('click', () => {
      window.HarrysExcel.openAddModal();
    });

    // Ribbon: Duplicate Row
    el.duplicateRowBtn.addEventListener('click', () => {
      if (!state.selectedRowId) {
        showToast('Please select a beverage row to duplicate first.', 'error');
        return;
      }
      window.HarrysExcel.duplicateRow(state.selectedRowId);
    });

    // Ribbon: Delete Row
    el.deleteRowBtn.addEventListener('click', () => {
      if (!state.selectedRowId) {
        showToast('Please select a beverage row to delete first.', 'error');
        return;
      }
      window.HarrysExcel.deleteRow(state.selectedRowId);
    });

    // Ribbon: Export XLSX
    el.exportXlsxBtn.addEventListener('click', () => {
      window.HarrysExcel.exportToXLSX();
    });

    // Ribbon: Export CSV
    el.exportCsvBtn.addEventListener('click', () => {
      window.HarrysExcel.exportToCSV();
    });

    // Ribbon: Import File
    el.importFileBtn.addEventListener('click', () => {
      el.fileInput.click();
    });
    
    el.fileInput.addEventListener('change', (e) => {
      window.HarrysExcel.handleFileImport(e);
    });

    // Ribbon: Print
    el.printSheetBtn.addEventListener('click', () => {
      setViewMode('training');
      setTimeout(() => {
        window.print();
      }, 150);
    });

    // Ribbon: Reset Catalog
    el.resetCatalogBtn.addEventListener('click', () => {
      if (confirm("Reset catalog to the official 276 ready-to-drink store master dataset?")) {
        state.drinks = JSON.parse(JSON.stringify(state.defaultDrinks));
        saveState();
        renderSheetTabs();
        filterAndRenderTable();
        renderTrainingSheet();
        showToast("Catalog reset to 276 ready-to-drink beverages", "success");
      }
    });

    // Ribbon: Planogram Rules
    el.trainingGuideBtn.addEventListener('click', () => {
      el.trainingModal.classList.add('active');
    });

    // Form Submit
    el.drinkForm.addEventListener('submit', (e) => {
      e.preventDefault();
      window.HarrysExcel.saveModalForm();
    });

    // Modal Close
    document.querySelectorAll('.excel-modal-close-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.excel-modal-backdrop').forEach(m => m.classList.remove('active'));
      });
    });

    document.querySelectorAll('.excel-modal-backdrop').forEach(m => {
      m.addEventListener('click', (e) => {
        if (e.target === m) m.classList.remove('active');
      });
    });
  }

  // Toast System
  function showToast(msg, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast-box';
    if (type === 'error') toast.style.borderLeftColor = '#EF4444';
    if (type === 'success') toast.style.borderLeftColor = '#10B981';
    
    toast.innerHTML = `<span>${type === 'error' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️'}</span> <span>${escapeHtml(msg)}</span>`;
    el.toastContainer.appendChild(toast);
    
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.2s ease';
      setTimeout(() => toast.remove(), 200);
    }, 2800);
  }

  // Helper Escape HTML
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Global API methods attached to window.HarrysExcel
  window.HarrysExcel = {
    openZoom: function (id) {
      const item = state.drinks.find(d => d.id === id);
      if (!item) return;
      el.zoomModalImg.src = item.image_path;
      el.zoomModalTitle.textContent = `${item.full_name} (${item.size})`;
      el.zoomModalSub.innerHTML = `
        <strong>Category:</strong> ${escapeHtml(item.category)} • <strong>Brand:</strong> ${escapeHtml(item.brand_group)}<br>
        <strong>Packaging:</strong> ${escapeHtml(item.packaging)} (${escapeHtml(item.container_type)})<br>
        <strong>myCoke SKU:</strong> #${escapeHtml(item.sku)} • <strong>UPC:</strong> ${escapeHtml(item.upc || 'N/A')}<br>
        <strong>Image File:</strong> <code style="font-size:10px; color:var(--harrys-red);">${escapeHtml(item.image_path.replace('drinks/', ''))}</code>
      `;
      el.zoomModal.classList.add('active');
    },

    openAddModal: function () {
      el.drinkModalTitle.innerHTML = `<span>➕</span> Insert New Beverage Row`;
      document.getElementById('form-drink-id').value = '';
      document.getElementById('form-drink-name').value = '';
      document.getElementById('form-drink-brand').value = '';
      document.getElementById('form-drink-category').value = 'Carbonated Soft Drinks';
      document.getElementById('form-drink-size').value = '20 oz';
      document.getElementById('form-drink-container').value = 'Plastic Bottle';
      document.getElementById('form-drink-pack').value = '24 Loose';
      document.getElementById('form-drink-sku').value = '';
      document.getElementById('form-drink-upc').value = '';
      document.getElementById('form-drink-zone').value = 'Door 1: Core Colas & Classic Soft Drinks';
      document.getElementById('form-drink-image').value = 'drinks/Coca_Cola_Original_Taste_20oz_Bottle.png';
      el.drinkModal.classList.add('active');
    },

    openEditModal: function (id) {
      const item = state.drinks.find(d => d.id === id);
      if (!item) return;
      el.drinkModalTitle.innerHTML = `<span>✏️</span> Edit Beverage Details`;
      document.getElementById('form-drink-id').value = item.id;
      document.getElementById('form-drink-name').value = item.full_name || '';
      document.getElementById('form-drink-brand').value = item.brand_group || '';
      document.getElementById('form-drink-category').value = item.category || 'Carbonated Soft Drinks';
      document.getElementById('form-drink-size').value = item.size || '';
      document.getElementById('form-drink-container').value = item.container_type || 'Plastic Bottle';
      document.getElementById('form-drink-pack').value = item.packaging || '';
      document.getElementById('form-drink-sku').value = item.sku || '';
      document.getElementById('form-drink-upc').value = item.upc || '';
      document.getElementById('form-drink-zone').value = item.cooler_zone || '';
      document.getElementById('form-drink-image').value = item.image_path || '';
      el.drinkModal.classList.add('active');
    },

    saveModalForm: function () {
      const id = document.getElementById('form-drink-id').value;
      const isNew = !id;
      
      const drinkObj = {
        id: isNew ? 'drink-' + Date.now() : id,
        full_name: document.getElementById('form-drink-name').value.trim(),
        brand_group: document.getElementById('form-drink-brand').value.trim(),
        category: document.getElementById('form-drink-category').value,
        size: document.getElementById('form-drink-size').value.trim(),
        container_type: document.getElementById('form-drink-container').value,
        packaging: document.getElementById('form-drink-pack').value.trim(),
        sku: document.getElementById('form-drink-sku').value.trim(),
        upc: document.getElementById('form-drink-upc').value.trim(),
        cooler_zone: document.getElementById('form-drink-zone').value.trim(),
        image_path: document.getElementById('form-drink-image').value.trim() || 'drinks/Coca_Cola_Original_Taste_20oz_Bottle.png',
        row_num: isNew ? state.drinks.length + 1 : undefined
      };

      if (isNew) {
        state.drinks.push(drinkObj);
        showToast(`Added "${drinkObj.full_name}" to catalog`, 'success');
      } else {
        const idx = state.drinks.findIndex(d => d.id === id);
        if (idx !== -1) {
          state.drinks[idx] = { ...state.drinks[idx], ...drinkObj };
          showToast(`Updated "${drinkObj.full_name}"`, 'success');
        }
      }

      el.drinkModal.classList.remove('active');
      saveState();
      renderSheetTabs();
      filterAndRenderTable();
    },

    duplicateRow: function (id) {
      const orig = state.drinks.find(d => d.id === id);
      if (!orig) return;
      
      const copy = JSON.parse(JSON.stringify(orig));
      copy.id = 'drink-' + Date.now();
      copy.full_name = orig.full_name + ' (Copy)';
      copy.sku = orig.sku + '-CPY';
      copy.row_num = state.drinks.length + 1;
      
      state.drinks.push(copy);
      state.selectedRowId = copy.id;
      saveState();
      renderSheetTabs();
      filterAndRenderTable();
      showToast(`Duplicated "${orig.full_name}"`, 'success');
    },

    deleteRow: function (id) {
      const item = state.drinks.find(d => d.id === id);
      if (!item) return;
      if (!confirm(`Are you sure you want to delete "${item.full_name}" (${item.size})?`)) return;

      state.drinks = state.drinks.filter(d => d.id !== id);
      if (state.selectedRowId === id) state.selectedRowId = null;
      
      saveState();
      renderSheetTabs();
      filterAndRenderTable();
      showToast(`Deleted "${item.full_name}"`, 'info');
    },

    clearFilters: function () {
      el.searchInput.value = '';
      state.searchQuery = '';
      state.currentSheet = 'ALL';
      state.currentBrandFilter = 'ALL';
      renderSheetTabs();
      renderFormulaPills();
      filterAndRenderTable();
    },

    // Native Microsoft Excel XLSX Export (with Multi-Category Sheets)
    exportToXLSX: function () {
      if (typeof XLSX === 'undefined') {
        showToast('SheetJS Excel library is loading...', 'error');
        return;
      }

      const wb = XLSX.utils.book_new();

      function formatRowsForExcel(items) {
        return items.map((d, i) => ({
          'Row #': i + 1,
          'Full Beverage Name': d.full_name,
          'Brand Family': d.brand_group,
          'Category': d.category,
          'Size': d.size,
          'Container': d.container_type,
          'Packaging / Case': d.packaging,
          'myCoke SKU': d.sku,
          'UPC Barcode': d.upc || '',
          'Cooler Planogram Zone': d.cooler_zone || '',
          'Drink Image Path': d.image_path
        }));
      }

      // 1. Master Sheet (All 276 items)
      const masterData = formatRowsForExcel(state.drinks);
      const wsMaster = XLSX.utils.json_to_sheet(masterData);
      wsMaster['!cols'] = [
        { wch: 6 }, { wch: 35 }, { wch: 22 }, { wch: 25 }, { wch: 10 },
        { wch: 15 }, { wch: 18 }, { wch: 12 }, { wch: 16 }, { wch: 38 }, { wch: 45 }
      ];
      XLSX.utils.book_append_sheet(wb, wsMaster, 'Master Catalog (All 276)');

      // 2. Department Category Sheets
      DEPARTMENT_CONFIG.forEach(dept => {
        let deptItems = [];
        if (Array.isArray(dept.category)) {
          deptItems = state.drinks.filter(d => dept.category.includes(d.category));
        } else {
          deptItems = state.drinks.filter(d => d.category === dept.category);
        }

        if (deptItems.length > 0) {
          const deptData = formatRowsForExcel(deptItems);
          const wsDept = XLSX.utils.json_to_sheet(deptData);
          wsDept['!cols'] = wsMaster['!cols'];
          XLSX.utils.book_append_sheet(wb, wsDept, dept.shortName.substring(0, 31));
        }
      });

      // Write & Download file
      XLSX.writeFile(wb, "Harrys_Beverage_Catalog_Master.xlsx");
      showToast('Downloaded Excel Workbook (.xlsx) with categorized sheets!', 'success');
    },

    // Export CSV
    exportToCSV: function () {
      let csv = 'Row,Name,Brand,Category,Size,Container,Packaging,SKU,UPC,Cooler_Zone,Image_Path\n';
      state.drinks.forEach((d, i) => {
        const row = [
          i + 1,
          `"${(d.full_name || '').replace(/"/g, '""')}"`,
          `"${(d.brand_group || '').replace(/"/g, '""')}"`,
          `"${(d.category || '').replace(/"/g, '""')}"`,
          `"${(d.size || '').replace(/"/g, '""')}"`,
          `"${(d.container_type || '').replace(/"/g, '""')}"`,
          `"${(d.packaging || '').replace(/"/g, '""')}"`,
          `"${(d.sku || '').replace(/"/g, '""')}"`,
          `"${(d.upc || '').replace(/"/g, '""')}"`,
          `"${(d.cooler_zone || '').replace(/"/g, '""')}"`,
          `"${(d.image_path || '').replace(/"/g, '""')}"`
        ];
        csv += row.join(',') + '\n';
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'harrys_drinks_inventory.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast('Exported CSV file', 'success');
    },

    // File Import (.xlsx, .csv, .json)
    handleFileImport: function (e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      const ext = file.name.split('.').pop().toLowerCase();

      reader.onload = function (evt) {
        try {
          if (ext === 'json') {
            const parsed = JSON.parse(evt.target.result);
            if (Array.isArray(parsed)) {
              state.drinks = parsed;
              saveState();
              renderSheetTabs();
              filterAndRenderTable();
              showToast(`Imported ${parsed.length} beverages from JSON`, 'success');
            }
          } else if (ext === 'xlsx' || ext === 'xls') {
            if (typeof XLSX === 'undefined') {
              showToast('Excel parser unavailable', 'error');
              return;
            }
            const data = new Uint8Array(evt.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(firstSheet);
            
            if (jsonData.length > 0) {
              state.drinks = jsonData.map((row, idx) => ({
                id: 'import-' + idx,
                full_name: row['Full Beverage Name'] || row['Name'] || row['full_name'] || 'Beverage',
                brand_group: row['Brand Family'] || row['Brand'] || row['brand_group'] || 'General',
                category: row['Category'] || row['category'] || 'Carbonated Soft Drinks',
                size: row['Size'] || row['size'] || '20 oz',
                container_type: row['Container'] || row['container_type'] || 'Plastic Bottle',
                packaging: row['Packaging / Case'] || row['Packaging'] || row['packaging'] || '24 Loose',
                sku: String(row['myCoke SKU'] || row['SKU'] || row['sku'] || idx + 100000),
                upc: String(row['UPC Barcode'] || row['UPC'] || row['upc'] || ''),
                cooler_zone: row['Cooler Planogram Zone'] || row['Zone'] || '',
                image_path: row['Drink Image Path'] || row['Image'] || 'drinks/Coca_Cola_Original_Taste_20oz_Bottle.png',
                row_num: idx + 1
              }));
              saveState();
              renderSheetTabs();
              filterAndRenderTable();
              showToast(`Imported ${state.drinks.length} items from Excel`, 'success');
            }
          }
        } catch (err) {
          console.error(err);
          showToast('Error importing file: ' + err.message, 'error');
        }
      };

      if (ext === 'xlsx' || ext === 'xls') {
        reader.readAsArrayBuffer(file);
      } else {
        reader.readAsText(file);
      }
      e.target.value = '';
    }
  };

  // Start application on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
