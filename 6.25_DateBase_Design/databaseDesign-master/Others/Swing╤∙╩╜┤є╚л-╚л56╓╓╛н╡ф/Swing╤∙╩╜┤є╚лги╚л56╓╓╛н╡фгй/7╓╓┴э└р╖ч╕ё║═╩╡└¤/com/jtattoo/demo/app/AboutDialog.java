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

import com.jtattoo.demo.utils.*;
import com.jtattoo.demo.images.*;

/**
 * @author  Michael Hagen
 */
public class AboutDialog extends JDialog {
    private Component parent = null;
    
    public AboutDialog(Component aParent) {
        super(JOptionPane.getFrameForComponent(aParent), "About", true);
        parent = aParent;
        init();
    }
    
    private void init() {
        JPanel contentPanel = new JPanel(new BorderLayout());
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setBorder(BorderFactory.createEmptyBorder());
        JPanel aboutPanel = new JPanel();
        aboutPanel.setBorder(BorderFactory.createEmptyBorder(32, 8, 8, 8));
        SplashPanel splashPanel = new SplashPanel();
        aboutPanel.add(splashPanel);
        tabbedPane.add("About", aboutPanel);
        
        if (!(parent instanceof JApplet)) {
            JPanel propertiesPanel = new JPanel(new BorderLayout());
            JTable propertiesTable = new JTable(new PropertiesTableModel());
            propertiesTable.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
            propertiesTable.setColumnSelectionAllowed(false);
            propertiesTable.setRowSelectionAllowed(false);
            propertiesTable.getColumnModel().getColumn(0).setPreferredWidth(188);
            propertiesTable.getColumnModel().getColumn(1).setPreferredWidth(418);
            propertiesPanel.add(new JScrollPane(propertiesTable), BorderLayout.CENTER);
            tabbedPane.add("Properties", propertiesPanel);
        }
        contentPanel.add(tabbedPane, BorderLayout.CENTER);
        setContentPane(contentPanel);
        showDlg();
    }
    
    private void showDlg() {
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        Dimension dlgSize = new Dimension(640, 480);
        int dlgPosX = (screenSize.width / 2) - (dlgSize.width / 2);
        int dlgPosY = (screenSize.height / 2) - (dlgSize.height / 2);
        setLocation(dlgPosX, dlgPosY);
        setSize(dlgSize);
        setVisible(true);
    }
    
    private class PropertiesTableModel extends AbstractTableModel {
        public int getColumnCount()
        { return 2; }
        
        public String getColumnName(int index) {
            if (index == 0)
                return "Property";
            else if (index == 1)
                return "Value";
            return "ERROR";
        }
        
        public int getRowCount()
        { return System.getProperties().size(); }
        
        public Object getValueAt(int rowIndex, int colIndex) {
            Iterator iter = System.getProperties().keySet().iterator();
            int i = 0;
            while (iter.hasNext()) {
                Object key = iter.next();
                if (i == rowIndex) {
                    if (colIndex == 0)
                        return key;
                    else
                        return System.getProperties().getProperty(key.toString());
                }
                i++;
            }
            return "ERROR";
        }
    }
}
