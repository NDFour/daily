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
public class ProgressBarPanel extends JPanel {
    private JProgressBar standardBar = null;
    private JProgressBar textBar = null;
    private JProgressBar disabledBar = null;
    
    private JProgressBar indeterminatedBar = null;
    
    public ProgressBarPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("ProgressBar");
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        GridBagLayout layout = new GridBagLayout();
        JPanel contentPanel = new JPanel(layout);
        
        standardBar = new JProgressBar(0, 100);
        standardBar.setValue(33);
        standardBar.setPreferredSize(new Dimension(140, 16));
        textBar = new JProgressBar(0, 100);
        textBar.setValue(50);
        textBar.setString("50%");
        textBar.setStringPainted(true);
        textBar.setPreferredSize(new Dimension(140, 16));
        disabledBar = new JProgressBar(0, 100);
        disabledBar.setValue(66);
        disabledBar.setEnabled(false);
        disabledBar.setPreferredSize(new Dimension(140, 16));
        
        if (JTattooUtilities.getJavaVersion() >= 1.4) {
            indeterminatedBar = new JProgressBar();
            indeterminatedBar.setString("indeterminated");
            indeterminatedBar.setStringPainted(true);
            indeterminatedBar.setIndeterminate(true);
            indeterminatedBar.setPreferredSize(new Dimension(140, 16));
        }
        
        GridBagHelper.addComponent(contentPanel, standardBar,       0, 1, 1, 1, 16, 4,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, textBar,           0, 2, 1, 1, 16, 4,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        GridBagHelper.addComponent(contentPanel, disabledBar,       0, 3, 1, 1, 16, 4,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
        if (JTattooUtilities.getJavaVersion() >= 1.4)
            GridBagHelper.addComponent(contentPanel, indeterminatedBar, 0, 4, 1, 1, 16, 4,  0.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);

        JScrollPane scrollPane = new JScrollPane(contentPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        add(scrollPane, BorderLayout.CENTER);
    }
    
    public void updateLookAndFeel() {
        if (JTattooUtilities.getJavaVersion() >= 1.4) {
            indeterminatedBar.setIndeterminate(false);
            indeterminatedBar.setIndeterminate(true);
        }
    }
}
