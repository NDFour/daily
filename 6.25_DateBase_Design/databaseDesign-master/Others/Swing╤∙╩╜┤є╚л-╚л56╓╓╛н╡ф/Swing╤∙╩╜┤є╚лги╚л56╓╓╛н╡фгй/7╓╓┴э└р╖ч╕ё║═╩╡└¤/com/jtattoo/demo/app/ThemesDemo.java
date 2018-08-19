/*
 * Copyright 2005 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.app;

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class ThemesDemo extends JFrame {
    public static ThemesDemo app = null;
    public JPopupMenu popup = null;
    
    public ThemesDemo() {
        super("Themes-Demo-Application");
        
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
        
        // setup the popup menu
        popup = new JPopupMenu();
        menuItem = new JMenuItem("undo");
        popup.add(menuItem);
        menuItem = new JMenuItem("redo");
        popup.add(menuItem);
        popup.addSeparator();
        menuItem = new JMenuItem("cut");
        popup.add(menuItem);
        menuItem = new JMenuItem("copy");
        popup.add(menuItem);
        menuItem = new JMenuItem("paste");
        popup.add(menuItem);
        menuItem = new JMenuItem("delete");
        popup.add(menuItem);
        
        // add the popup to the editor pane
        editor.addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                maybeShowPopup(e);
            }
            
            public void mouseReleased(MouseEvent e) {
                maybeShowPopup(e);
            }
            
            private void maybeShowPopup(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    popup.show(e.getComponent(), e.getX(), e.getY());
                }
            }
        });
        
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
    } // end CTor SwingApplication
    
    public static void main(String[] args) {
        try {
            // setup the look and feel properties
            Properties props = new Properties();
            
            props.put("logoString", "my company"); 
            props.put("licenseKey", "INSERT YOUR LICENSE KEY HERE");
            
            props.put("selectionBackgroundColor", "180 240 197"); 
            props.put("menuSelectionBackgroundColor", "180 240 197"); 
            
            props.put("controlColor", "218 254 230");
            props.put("controlColorLight", "218 254 230");
            props.put("controlColorDark", "180 240 197"); 

            props.put("buttonColor", "218 230 254");
            props.put("buttonColorLight", "255 255 255");
            props.put("buttonColorDark", "244 242 232");

            props.put("rolloverColor", "218 254 230"); 
            props.put("rolloverColorLight", "218 254 230"); 
            props.put("rolloverColorDark", "180 240 197"); 

            props.put("windowTitleForegroundColor", "0 0 0");
            props.put("windowTitleBackgroundColor", "180 240 197"); 
            props.put("windowTitleColorLight", "218 254 230"); 
            props.put("windowTitleColorDark", "180 240 197"); 
            props.put("windowBorderColor", "218 254 230");
            
            // set your theme
            com.jtattoo.plaf.smart.SmartLookAndFeel.setCurrentTheme(props);
            // select the Look and Feel
            UIManager.setLookAndFeel("com.jtattoo.plaf.smart.SmartLookAndFeel");
            
            app = new ThemesDemo();
        }
        catch (Exception ex) {
            ex.printStackTrace();
        }
    } // end main
    
} // end class SwingApplication
    