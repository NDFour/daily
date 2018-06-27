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
public class TextAreaPanel extends JPanel {
    private JTextArea standardTextArea = null;
    private JTextArea nonEditableTextArea = null;
    private JTextArea disabledTextArea = null;
    private JTextArea coloredTextArea = null;
    
    public TextAreaPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("TextArea");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        GridBagLayout layout = new GridBagLayout();
        JPanel contentPanel = new JPanel(layout);
        
        standardTextArea = new JTextArea("Standard");
        JScrollPane standardScrollPane = new JScrollPane(standardTextArea);
        standardScrollPane.setPreferredSize(new Dimension(320, 80));
        nonEditableTextArea = new JTextArea("Non editable");
        nonEditableTextArea.setEditable(false);
        JScrollPane nonEditableScrollPane = new JScrollPane(nonEditableTextArea);
        nonEditableScrollPane.setPreferredSize(new Dimension(320, 80));
        disabledTextArea = new JTextArea("Disabled");
        disabledTextArea.setEnabled(false);
        JScrollPane disabledScrollPane = new JScrollPane(disabledTextArea);
        disabledScrollPane.setPreferredSize(new Dimension(320, 80));
        coloredTextArea = new JTextArea("Colored");
        coloredTextArea.setForeground(Color.green);
        coloredTextArea.setBackground(new Color(128, 128, 255));
        JScrollPane coloredScrollPane = new JScrollPane(coloredTextArea);
        coloredScrollPane.setPreferredSize(new Dimension(320, 80));
        JEditorPane editorPane = new JEditorPane("text/html","<html>This is a <b>HTML</b> text!</html>");
        JScrollPane editorScrollPane = new JScrollPane(editorPane);
        editorScrollPane.setPreferredSize(new Dimension(320, 80));
        
        JLabel standardLabel = new JLabel("Standard:");
        JLabel nonEditableLabel = new JLabel("Non editable:");
        JLabel disabledLabel = new JLabel("Disabled:");
        JLabel coloredLabel = new JLabel("Colored:");
        JLabel editorLabel = new JLabel("JEditorPane:");
        
        GridBagHelper.addComponent(contentPanel, standardLabel,         0, 1, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, standardScrollPane,    1, 1, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, nonEditableLabel,      0, 2, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, nonEditableScrollPane, 1, 2, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledLabel,         0, 3, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledScrollPane,    1, 3, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, coloredLabel,          0, 4, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, coloredScrollPane,     1, 4, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, editorLabel,           0, 5, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, editorScrollPane,      1, 5, 1, 1, 16, 0,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        JScrollPane scrollPane = new JScrollPane(contentPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        add(scrollPane, BorderLayout.CENTER);
    }
}
