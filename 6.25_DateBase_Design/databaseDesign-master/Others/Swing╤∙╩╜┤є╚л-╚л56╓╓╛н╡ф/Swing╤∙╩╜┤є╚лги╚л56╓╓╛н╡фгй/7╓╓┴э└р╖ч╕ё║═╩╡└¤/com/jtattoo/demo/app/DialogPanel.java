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
public class DialogPanel extends JPanel {
    private Component parent = null;
    private JButton informationButton = null;
    private JButton confirmationButton = null;
    private JButton warningButton = null;
    private JButton errorButton = null;
    private JButton nativeFileChooserButton = null;
    private JButton fileChooserButton = null;
    private JButton colorChooserButton = null;
    private FileDialog fileDialog = null;
    
    public DialogPanel(Component aParent) {
        super(new BorderLayout());
        parent = aParent;
        init();
    }
    
    private void init() {
        setName("Dialogs");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        
        informationButton = new JButton("Information dialog");
        informationButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(parent, "Information dialog", "Information", JOptionPane.INFORMATION_MESSAGE);
            }
        });
        confirmationButton = new JButton("Confirmation dialog");
        confirmationButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(parent, "Confirmation dialog", "Confirmation", JOptionPane.QUESTION_MESSAGE);
            }
        });
        warningButton = new JButton("Warning dialog");
        warningButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(parent, "Warning dialog", "Warning", JOptionPane.WARNING_MESSAGE);
            }
        });
        errorButton = new JButton("Error dialog");
        errorButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(parent, "Error dialog", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        nativeFileChooserButton = new JButton("Native FileChooser dialog");
        nativeFileChooserButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                fileDialog = new FileDialog(JOptionPane.getFrameForComponent(parent), "Open File");
                fileDialog .setResizable(true);
                fileDialog .setVisible(true);
            }
        });
        fileChooserButton = new JButton("FileChooser dialog");
        fileChooserButton.setEnabled(!(parent instanceof JApplet));
        fileChooserButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JFileChooser fc = new JFileChooser();
                int result = fc.showOpenDialog(parent);
            }
        });
        colorChooserButton = new JButton("ColorChooser dialog");
        colorChooserButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                Color c = JColorChooser.showDialog(parent, "JColorChooser", Color.blue);
            }
        });
        
        JPanel contentPanel = new JPanel(new GridBagLayout());
        GridBagHelper.addComponent(contentPanel, informationButton,         0, 0, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, confirmationButton,        0, 1, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, warningButton,             0, 2, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, errorButton,               0, 3, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, nativeFileChooserButton,   0, 4, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, fileChooserButton,         0, 5, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, colorChooserButton,        0, 6, 1, 1, 16, 8, 0, 4, 0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);

        JScrollPane scrollPane = new JScrollPane(contentPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        add(scrollPane, BorderLayout.CENTER);
    }
    
}
