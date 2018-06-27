/*
 * Copyright 2005 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.app;

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
import javax.swing.border.*;
import javax.swing.plaf.*;

import com.jtattoo.plaf.*;
import com.jtattoo.border.*;
import com.jtattoo.demo.utils.*;

/**
 *
 * @author  Michael Hagen
 */
public class WidgetPanel extends JPanel {
    private JPanel widgetPanel = null;
    private JScrollPane tablePanel = null;
    private JSplitPane splitPane = null;
    
    private JComboBox addressCombo = null;
    private JTextField firstNameField = null;
    private JTextField lastNameField = null;
    private JTextField streetField = null;
    private JTextField cityField = null;
    private ButtonGroup buttonGroup = null;
    private JRadioButton redButton = null;
    private JRadioButton greenButton = null;
    private JRadioButton blueButton = null;
    private JCheckBox bananaButton = null;
    private JCheckBox burgerButton = null;
    private JCheckBox icecreamButton = null;
    
    private JButton updateButton = null;
    private JButton insertButton = null;
    private JButton deleteButton = null;
    private JTable  table = null;
    
    private ArrayList colNames = new ArrayList();
    private ArrayList dataList = new ArrayList();
    
    public WidgetPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("Form");
        initModel();
        initControls();
    }
    
    private void initModel() {
        colNames.add("Salutation");
        colNames.add("Firstname");
        colNames.add("Lastname");
        colNames.add("Street");
        colNames.add("City");
        colNames.add("Male");
        
        ArrayList rowData = new ArrayList();
        rowData.add("Mr.");
        rowData.add("Mad");
        rowData.add("Meier");
        rowData.add("Eastend 17");
        rowData.add("New York");
        rowData.add(Boolean.TRUE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Mrs.");
        rowData.add("Georgia");
        rowData.add("Smith");
        rowData.add("Westend 12");
        rowData.add("New York");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Sir");
        rowData.add("Edward");
        rowData.add("Hillary");
        rowData.add("Parkavenue 1a");
        rowData.add("Los Angeles");
        rowData.add(Boolean.TRUE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Mr.");
        rowData.add("Ronald");
        rowData.add("Mc. Guire");
        rowData.add("13th Street");
        rowData.add("Newmark");
        rowData.add(Boolean.TRUE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Mrs.");
        rowData.add("Martina");
        rowData.add("Diego");
        rowData.add("Block A");
        rowData.add("Westpoint");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Lady");
        rowData.add("Bettina");
        rowData.add("Maradona");
        rowData.add("Eastwoodpark 44");
        rowData.add("Washington");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Herr");
        rowData.add("Albert");
        rowData.add("Dreistein");
        rowData.add("Burgstrasse 22");
        rowData.add("Koeln");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Frau");
        rowData.add("Roberta");
        rowData.add("Robinson");
        rowData.add("Gartenstr. 22");
        rowData.add("Kleinkleckersdorf");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Herr");
        rowData.add("Manfred");
        rowData.add("Mustermann");
        rowData.add("Schlossplatz 22");
        rowData.add("Schwaebisch Gmuend");
        rowData.add(Boolean.TRUE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Herr");
        rowData.add("Norbert");
        rowData.add("Noergler");
        rowData.add("Wallstr 1a");
        rowData.add("Oberammergau");
        rowData.add(Boolean.TRUE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Frau");
        rowData.add("Lischen");
        rowData.add("Mueller");
        rowData.add("Kleintalweg 16");
        rowData.add("Witzenhausen");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
        
        rowData = new ArrayList();
        rowData.add("Frau");
        rowData.add("Lotte");
        rowData.add("Lustig");
        rowData.add("Preussenalee 1a");
        rowData.add("Krauthausen");
        rowData.add(Boolean.FALSE);
        dataList.add(rowData);
    }
    
    private void initControls() {
        widgetPanel = createWidgetPanel();
        tablePanel = createTablePanel();
        splitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, true, widgetPanel, tablePanel);
        splitPane.setDividerLocation(320);
        add(splitPane, BorderLayout.CENTER);
        
        deleteButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
//                TableColumn aColumn = table.getTableHeader().getColumnModel().getColumn(0); 
//                TableCellRenderer renderer = aColumn.getHeaderRenderer(); 
//                System.out.println("renderer: " + renderer);
//                System.out.println("defaultRenderer: " + table.getTableHeader().getDefaultRenderer());
            }
        });
                
    }
    
    private JPanel createWidgetPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.add(createFormPanel(), BorderLayout.CENTER);
        panel.add(createButtonPanel(), BorderLayout.EAST);
        return panel;
    }
    
    private JScrollPane createFormPanel() {
        addressCombo = new JComboBox(new String[] {"Mr.", "Mrs.", "Sir", "Lady", "Herr", "Frau"} );
        firstNameField = new JTextField();
        lastNameField = new JTextField();
        streetField = new JTextField();
        cityField = new JTextField();
        
        JPanel radioPanel = new JPanel(new BorderLayout());
        radioPanel.setBorder(JTBorderFactory.createTitleBorder("favorite color"));
        redButton = new JRadioButton("red");
        greenButton = new JRadioButton("green");
        blueButton = new JRadioButton("blue");
        radioPanel.add(redButton, BorderLayout.NORTH);
        radioPanel.add(greenButton, BorderLayout.CENTER);
        radioPanel.add(blueButton, BorderLayout.SOUTH);
        buttonGroup = new ButtonGroup();
        buttonGroup.add(redButton);
        buttonGroup.add(greenButton);
        buttonGroup.add(blueButton);
        redButton.setSelected(true);
        
        JPanel checkPanel = new JPanel(new BorderLayout());
        checkPanel.setBorder(JTBorderFactory.createTitleBorder("favorite food"));
        bananaButton = new JCheckBox("bananas");
        burgerButton = new JCheckBox("hamburgers");
        icecreamButton = new JCheckBox("icecream");
        checkPanel.add(bananaButton, BorderLayout.NORTH);
        checkPanel.add(burgerButton, BorderLayout.CENTER);
        checkPanel.add(icecreamButton, BorderLayout.SOUTH);
        
        JPanel panel = new JPanel(new GridBagLayout());
        //panel.setOpaque(false);
        JPanel topDistPanel = new JPanel();
        JPanel bottomDistPanel = new JPanel();
        GridBagHelper.addComponent(panel, topDistPanel,            0, 0, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.NORTHWEST);
        
        GridBagHelper.addComponent(panel, new JLabel("Salutation"),0, 1, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, addressCombo,            1, 1, 1, 1, 0, 0, 0.3, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTHWEST);
        GridBagHelper.addComponent(panel, new JPanel(),            2, 1, 1, 1, 0, 0, 0.7, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
        
        GridBagHelper.addComponent(panel, new JLabel("Firstname"), 0, 2, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, firstNameField,          1, 2, 3, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, new JLabel("Lastname"),  0, 3, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, lastNameField,           1, 3, 3, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, new JLabel("Street"),    0, 4, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, streetField,             1, 4, 3, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, new JLabel("City"),      0, 5, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, cityField,               1, 5, 3, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
        
        GridBagHelper.addComponent(panel, radioPanel,              0, 6, 2, 1, 0, 0, 0.0, 0.0, GridBagConstraints.BOTH, GridBagConstraints.WEST);
        GridBagHelper.addComponent(panel, checkPanel,              2, 6, 1, 1, 0, 0, 0.0, 0.0, GridBagConstraints.BOTH, GridBagConstraints.WEST);
        
        GridBagHelper.addComponent(panel, bottomDistPanel,         0, 10, 1, 1, 0, 0, 0.0, 1.0, GridBagConstraints.VERTICAL, GridBagConstraints.NORTHWEST);

        JScrollPane scrollPane = new JScrollPane(panel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        return scrollPane;
    }
    
    private JScrollPane createButtonPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        updateButton = new JButton("update");
        updateButton.setDefaultCapable(true);
        insertButton = new JButton("insert");
        deleteButton = new JButton("delete");
        
        GridBagHelper.setMinRowHeight(panel, 0, 8);
        GridBagHelper.setMinColWidth(panel, 0, 100);
        GridBagHelper.addComponent(panel, updateButton, 0, 1, 1, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTHWEST);
        GridBagHelper.addComponent(panel, insertButton, 0, 2, 1, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTHWEST);
        GridBagHelper.addComponent(panel, deleteButton, 0, 3, 1, 1, 0, 0, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTHWEST);
        GridBagHelper.addComponent(panel, new JPanel(), 0, 4, 1, 1, 0, 0, 0.0, 1.0, GridBagConstraints.VERTICAL,   GridBagConstraints.NORTHWEST);

        JScrollPane scrollPane = new JScrollPane(panel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        
        return scrollPane;
    }
    
    private JScrollPane createTablePanel() {
        MyTableModel model = new MyTableModel();
        table = new JTable(model);
        TableColumn tableCol = table.getColumnModel().getColumn(5);
        tableCol.setCellRenderer(new CheckBoxRenderer());
        tableCol.setPreferredWidth(30);
        
        return new JScrollPane(table);
    }
    
    public void setVisible(boolean aFlag) {
        super.setVisible(aFlag);
        if ((aFlag == true) && (getRootPane() != null)) {
            getRootPane().setDefaultButton(updateButton);
        }
    }
    
    private class MyTableModel extends AbstractTableModel {
        public int getColumnCount() {
            return colNames.size();
        }
        
        public String getColumnName(int index) {
            return (String)colNames.get(index);
        }
        
        public int getRowCount() {
            return dataList.size();
        }
        
        public Object getValueAt(int rowIndex, int colIndex) {
            if (rowIndex < dataList.size()) {
                ArrayList rowData = (ArrayList)dataList.get(rowIndex);
                if (colIndex < rowData.size()) {
                    return rowData.get(colIndex);
                }
            }
            return "ERROR";
        }
    }

//------------------------------------------------------------------------------    
    class CheckBoxRenderer extends DefaultTableCellRenderer {
        
        public Component getTableCellRendererComponent(JTable jTable, Object obj, boolean isSelected, boolean hasFocus, int row, int col) {
            JCheckBox checkBox = new JCheckBox("");
            checkBox.setOpaque(true);
            checkBox.setForeground(jTable.getForeground());
            checkBox.setBackground(jTable.getBackground());
            checkBox.setHorizontalAlignment(JCheckBox.CENTER);
            if (isSelected) {
                checkBox.setForeground(jTable.getSelectionForeground());
                Color bc = new Color(jTable.getSelectionBackground().getRGB());
                checkBox.setBackground(bc);
            }
            if (obj instanceof Boolean) {
                checkBox.setSelected(((Boolean)obj).booleanValue());
            }
            return checkBox;
        }
    }
}
