/*
 * Copyright 2005 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.app;

import java.awt.*;
import javax.swing.*;
import javax.swing.table.*;

/**
 *
 * @author  Michael Hagen
 */
public class TablePanel extends JPanel {
    private JTable table = null;
    
    public TablePanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("Table");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        MyTableModel tableModel = new MyTableModel();
        table = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(table);
        add(scrollPane, BorderLayout.CENTER);

        TableColumn tableCol = table.getColumnModel().getColumn(2);
        JComboBox comboBox = new JComboBox();
        comboBox.addItem("Snowboarding");
        comboBox.addItem("Rowing");
        comboBox.addItem("Chasing toddlers");
        comboBox.addItem("Speed reading");
        comboBox.addItem("Teaching high school");
        comboBox.addItem("None");
        tableCol.setCellEditor(new DefaultCellEditor(comboBox));
        tableCol.setPreferredWidth(200);
        
        tableCol = table.getColumnModel().getColumn(1);
        tableCol.setPreferredWidth(80);
    }

//---------------------------------------------------------------------------------------
    class MyTableModel extends AbstractTableModel {
        private String[] columnNames = {"First Name", "Last Name", "Sport", "# of Years", "Vegetarian"};
        private Object[][] data = {
            {"Mary", "Campione", "Snowboarding", new Integer(5), new Boolean(false)},
            {"Alison", "Huml", "Rowing", new Integer(3), new Boolean(true)},
            {"Kathy", "Walrath", "Knitting", new Integer(2), new Boolean(false)},
            {"Sharon", "Zakhour", "Speed reading", new Integer(20), new Boolean(true)},
            {"Philip", "Milne", "Pool", new Integer(10), new Boolean(false)}
        };

        public int getColumnCount() {
            return columnNames.length;
        }

        public int getRowCount() {
            return data.length;
        }

        public String getColumnName(int col) {
            return columnNames[col];
        }

        public Object getValueAt(int row, int col) {
            return data[row][col];
        }

        /*
         * JTable uses this method to determine the default renderer/
         * editor for each cell. If we didn't implement this method,
         * then the last column would contain text ("true"/"false"),
         * rather than a check box.
         */
        public Class getColumnClass(int c) {
            return getValueAt(0, c).getClass();
        }

        /*
         * Don't need to implement this method unless your table's editable.
         */
        public boolean isCellEditable(int row, int col) {
            return true;
        }

        /*
         * Don't need to implement this method unless your table's data can change.
         */
        public void setValueAt(Object value, int row, int col) {
            data[row][col] = value;
            fireTableCellUpdated(row, col);
        }

    }
    
}
