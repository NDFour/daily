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

/**
 *
 * @author  Michael Hagen
 */
public class ButtonPanel extends JPanel {
    private JButton standardButton = null;
    private JButton defaultButton = null;
    private JButton htmlButton = null;
    private JButton disabledButton = null;
    private JButton coloredButton = null;
    
    public ButtonPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("Buttons");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        GridBagLayout layout = new GridBagLayout();
        JPanel contentPanel = new JPanel(layout);
        
        standardButton = new JButton("Standard");
        
        defaultButton = new JButton("Default");
        defaultButton.setDefaultCapable(true);
        
        htmlButton = new JButton("<html><b>HTML</b>-Button</html>");
        
        disabledButton = new JButton("Disabled");
        disabledButton.setEnabled(false);
        
        coloredButton = new JButton("Colored");
        coloredButton.setForeground(new Color(128, 255, 128));
        coloredButton.setBackground(new Color(128, 128, 255));
        
        GridBagHelper.addComponent(contentPanel, standardButton,  0, 1, 1, 1, 16, 8,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, defaultButton,   0, 2, 1, 1, 16, 8,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, htmlButton,      0, 3, 1, 1, 16, 8,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledButton,  0, 4, 1, 1, 16, 8,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, coloredButton,   0, 5, 1, 1, 16, 8,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        JScrollPane scrollPane = new JScrollPane(contentPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        add(scrollPane, BorderLayout.CENTER);
    }
    
    public void setVisible(boolean aFlag) {
        super.setVisible(aFlag);
        if ((aFlag == true) && (getRootPane() != null)) {
            getRootPane().setDefaultButton(defaultButton);
        }
    }
}
