/*
 * Copyright 2006 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.app;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class SimpleThemesDemo extends JFrame {
    
    public SimpleThemesDemo() {
        super("SimpleThemesDemo-Application");
        
        // setup menu
        JMenuBar menuBar = new JMenuBar();
        JMenu menu = new JMenu("File");
        menu.setMnemonic('F');
        JMenuItem menuItem = new JMenuItem("New");
        menu.add(menuItem);
        menuItem = new JMenuItem("Open");
        menu.add(menuItem);
        menuItem = new JMenuItem("Save");
        menu.add(menuItem);
        menuItem = new JMenuItem("Save as");
        menu.add(menuItem);
        menu.addSeparator();
        menuItem = new JMenuItem("Exit");
        menuItem.setMnemonic('x');
        menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_F4, KeyEvent.ALT_MASK));
        menuItem.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent event) {
                System.exit(0);
            }
        });
        menu.add(menuItem);
        menuBar.add(menu);
        setJMenuBar(menuBar);
        
        // setup the widgets
        JPanel contentPanel = new JPanel(new BorderLayout());
        contentPanel.setBorder(BorderFactory.createEmptyBorder(0, 4, 4, 4));
        JTree tree = new JTree();
        tree.expandRow(3);
        tree.expandRow(2);
        tree.expandRow(1);
        JScrollPane westPanel = new JScrollPane(tree);
        JEditorPane editor = new JEditorPane("text/plain", "Hello World");
        JScrollPane eastPanel = new JScrollPane(editor);
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, true, westPanel,eastPanel);
        splitPane.setDividerLocation(148);
        contentPanel.add(splitPane, BorderLayout.CENTER);
        setContentPane(contentPanel);
        
        // add the listeners
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });
        
        // show the application
        setLocation(32, 32);
        setSize(400, 300);
        setVisible(true);
    } // end CTor SimpleThemesDemo
    
    public static void main(String[] args) {
        try {
            
            // setTheme(String themeName, String licenseKey, String logoString)
            com.jtattoo.plaf.acryl.AcrylLookAndFeel.setTheme("Green", "INSERT YOUR LICENSE KEY HERE", "my company");
            
            // select the Look and Feel
            UIManager.setLookAndFeel("com.jtattoo.plaf.acryl.AcrylLookAndFeel");
            
            // start the demo application
            new SimpleThemesDemo();
            
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    } // end main
    
} // end class SimpleThemesDemo
