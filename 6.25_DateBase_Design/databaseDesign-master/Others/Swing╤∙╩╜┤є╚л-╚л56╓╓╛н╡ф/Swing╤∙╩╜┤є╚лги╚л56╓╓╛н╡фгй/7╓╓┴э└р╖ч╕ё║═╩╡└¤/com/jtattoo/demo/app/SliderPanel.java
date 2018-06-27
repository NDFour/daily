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
 * @author Michael Hagen
 */
public class SliderPanel extends JPanel {
    private ImagePanel imagePanel = null;
    private JSlider horZoomSlider = null;
    private JSlider verZoomSlider = null;
    
    public SliderPanel() {
        super(new BorderLayout());
        init();
    }
    
    private void init() {
        setName("Sliders");
        setBorder(BorderFactory.createEmptyBorder(4, 4, 4, 4));
        imagePanel = new ImagePanel();
        horZoomSlider = new JSlider(JSlider.HORIZONTAL, 50, 200, 100);
        horZoomSlider.setMajorTickSpacing(10);
        horZoomSlider.setMinorTickSpacing(5);
        horZoomSlider.setPaintLabels(true);
        horZoomSlider.setPaintTicks(true);
        horZoomSlider.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                imagePanel.setHorScale(((JSlider)e.getSource()).getValue());
            }
        });
        verZoomSlider = new JSlider(JSlider.VERTICAL, 50, 200, 100);
        verZoomSlider.setMajorTickSpacing(10);
        verZoomSlider.setMinorTickSpacing(5);
        verZoomSlider.setPaintLabels(true);
        verZoomSlider.setPaintTicks(true);
        verZoomSlider.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                imagePanel.setVerScale(((JSlider)e.getSource()).getValue());
            }
        });
        add(imagePanel, BorderLayout.CENTER);
        add(horZoomSlider, BorderLayout.SOUTH);
        add(verZoomSlider, BorderLayout.EAST);
    }
    
    private class ImagePanel extends JPanel {
        private ImageIcon fishImage = ImageHelper.loadImage("fish.gif");
        private int horScale = 100;
        private int verScale = 100;
        
        public ImagePanel() {
            super();
            setBackground(Color.white);
        }
        
        public void setHorScale(int scale) {
            horScale = scale;
            repaint();
        }
        
        public void setVerScale(int scale) {
            verScale = scale;
            repaint();
        }
        
        public void paint(Graphics g) {
            int w = getWidth();
            int h = getHeight();
            int wi = fishImage.getIconWidth() * horScale / 100;
            int hi = fishImage.getIconHeight() * verScale / 100;
            int x = (w - wi) / 2;
            int y = (h - hi) / 2;
            g.setColor(getBackground());
            g.fillRect(0, 0, w, h);
            g.drawImage(fishImage.getImage(), x, y, wi, hi, getBackground(), null);
        }
    }
}
