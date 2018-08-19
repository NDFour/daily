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

import com.jtattoo.plaf.*;
import com.jtattoo.demo.utils.*;

/**
 *
 * @author  Michael Hagen
 */
public class TextFieldPanel extends JPanel {
    private JTextField standardField = null;
    private JTextField nonEditableField = null;
    private JTextField disabledField = null;
    private JTextField coloredField = null;
    private JPasswordField passwordField = null;
    
    public TextFieldPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("TextField");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        GridBagLayout layout = new GridBagLayout();
        JPanel contentPanel = new JPanel(layout);
        
        standardField = new JTextField("Standard");
        nonEditableField = new JTextField("Non editable");
        nonEditableField.setEditable(false);
        disabledField = new JTextField("Disabled");
        disabledField.setEnabled(false);
        coloredField = new JTextField("Colored");
        coloredField.setForeground(Color.green);
        coloredField.setBackground(new Color(128, 128, 255));
        passwordField = new JPasswordField("password");
        
        JLabel standardLabel = new JLabel("Standard:");
        JLabel nonEditableLabel = new JLabel("Non editable:");
        JLabel disabledLabel = new JLabel("Disabled:");
        JLabel coloredLabel = new JLabel("Colored:");
        JLabel passwordLabel = new JLabel("Password:");
        
        GridBagHelper.addComponent(contentPanel, standardLabel,    0, 1, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, standardField,    1, 1, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, nonEditableLabel, 0, 2, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, nonEditableField, 1, 2, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledLabel,    0, 3, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledField,    1, 3, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, coloredLabel,     0, 4, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, coloredField,     1, 4, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, passwordLabel,    0, 5, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, passwordField,    1, 5, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        JScrollPane scrollPane = new JScrollPane(contentPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        add(scrollPane, BorderLayout.CENTER);
    }
}
