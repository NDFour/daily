/*
 * Copyright 2005 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.utils;

import java.awt.*;
import javax.swing.*;

/** Hilfsklasse fuer das Einfuegen von Swing-Komponenten in ein Panel mit GridBagLayout.
 * @author Michael Hagen
 */
public final class GridBagHelper {
    private static final int MAXGRIDX = 511; // Eigentlich GridBagLayout.MAXGRIDX
    private static final int MAXGRIDY = 511; // Eigentlich GridBagLayout.MAXGRIDY
    private static final int VER_SEP_DIST = 4;
    private static final int HOR_FIELD_DIST = 4;
    private static final int VER_FIELD_DIST = 2;
    
    private GridBagHelper() {
        super();
    }
    
    /** Methode zum Einfuegen einer Komponente in ein Panel mit GridBagLayout.
     * Diese Methode erfrodert zwar eine Menge Parameter, ist aber immer
     * noch besser als den ganzen Salmon fuer jede Komponente erneut hinzuschreiben.
     * @param panel Panel in das eingefuegt werden soll
     * @param c Komponente die eingefuegt werden soll
     * @param x Spalte in der eingefuegt werden soll
     * @param y Zeile in die eingefuegt werden soll
     * @param width Breite der Komponente in Spalten
     * @param height Hoehe der Komponente in Zeilen
     * @param ipadx Anzahl Pixel die der minimalen Komponentenbreite hinzugefuegt wird
     * @param ipady Anzahl Pixel die der minimalen Komponentenhoehe hinzugefuegt wird
     * @param weightx Mass fuer die zusaetzliche Flaeche in horizontaler Richtung die dieser Komponente ggf. zur Verfuegung gestellt wird
     * @param weighty Mass fuer die zusaetzliche Flaeche in vertikaler Richtung die dieser Komponente ggf. zur Verfuegung gestellt wird
     * @param fill Art und Weise in der die Komponente zusaetzlichen Platz nutzt
     * @param anchor Position innerhalb der virtuellen Zelle (Zeile/Spalte) an der die Komponente festgemacht wird
     */
    public static void addComponent(
        JPanel panel,
        Component c,
        int x, int y, int width, int height,
        int ipadx, int ipady,
        double weightx, double weighty,
        int fill, int anchor) 
    {
        int dx = 0;
        int dy = 0;
        if (c instanceof JSeparator) {
            dy = VER_SEP_DIST;
        }
        else {
            dx = HOR_FIELD_DIST;
            dy = VER_FIELD_DIST;
        }
        addComponent(panel, c, x, y, width, height, ipadx, ipady, dx, dy, weightx, weighty, fill, anchor);
    }
    /** Einfuegen von Komponenten in ein Gridbaglayout
     * @param panel Panel in das eingefuegt werden soll
     * @param c Komponente die eingefuegt werden soll
     * @param x Spalte in der eingefuegt werden soll
     * @param y Zeile in die eingefuegt werden soll
     * @param width Breite der Komponente in Spalten
     * @param height Hoehe der Komponente in Zeilen
     * @param ipadx Anzahl Pixel die der minimalen Komponentenbreite hinzugefuegt wird
     * @param ipady Anzahl Pixel die der minimalen Komponentenhoehe hinzugefuegt wird
     * @param dx Horizontaler Abstand zu Nachbarkomponenten in Pixeln
     * @param dy Vertikaler Abstand zu Nachbarkomponenten in Pixeln
     * @param weightx Mass fuer die zusaetzliche Flaeche in horizontaler Richtung die dieser Komponente ggf. zur Verfuegung gestellt wird
     * @param weighty Mass fuer die zusaetzliche Flaeche in vertikaler Richtung die dieser Komponente ggf. zur Verfuegung gestellt wird
     * @param fill Art und Weise in der die Komponente zusaetzlichen Platz nutzt
     * @param anchor Position innerhalb der virtuellen Zelle (Zeile/Spalte) an der die Komponente festgemacht wird
     */
    public static void addComponent(
        JPanel panel,
        Component c,
        int x, int y, int width, int height,
        int ipadx, int ipady,
        int dx, int dy,
        double weightx, double weighty,
        int fill, int anchor) 
    {
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = x;
        gbc.gridy = y;
        gbc.gridwidth = width;
        gbc.gridheight = height;
        gbc.ipadx = (c instanceof JComboBox) ? Math.max(4, ipadx) : ipadx;
        gbc.ipady = (c instanceof JTextField) ? Math.max(6, ipady) : ipady;
        gbc.insets = new Insets(dy, dx, dy, dx);
        gbc.weightx = weightx;
        gbc.weighty = weighty;
        gbc.fill = fill;
        gbc.anchor = anchor;
        
        panel.add(c, gbc);
    }
    
    /**
     * Methode um eine Spalte in einem Panel mit GridBagLayout auf eine
     * feste Breite einzustellen.
     * @param panel Panel das eingestellt werden soll
     * @param col Spalte die eingestellt werden soll
     * @param width Breite in Pixeln
     */
    public static void setMinColWidth(JPanel panel, int col, int width) {
        JPanel sizePanel = new JPanel();
        sizePanel.setOpaque(false);
        sizePanel.setMinimumSize(new Dimension(width, 1));
        sizePanel.setPreferredSize(new Dimension(width, 1));
        sizePanel.setMaximumSize(new Dimension(width, 1));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.anchor = GridBagConstraints.WEST;
        gbc.gridx = col;
        gbc.gridy = MAXGRIDY;
        panel.add(sizePanel, gbc);
    }
    /**
     * Methode um eine Zeile in einem Panel mit GridBagLayout auf eine
     * feste Hoehe einzustellen.
     * @param panel Panel das eingestellt werden soll
     * @param row Zeile die eingestellt werden soll
     * @param height Hoehe in Pixeln
     */
    public static void setMinRowHeight(JPanel panel, int row, int height) {
        JPanel sizePanel = new JPanel();
        sizePanel.setOpaque(false);
        sizePanel.setMinimumSize(new Dimension(1, height));
        sizePanel.setPreferredSize(new Dimension(1, height));
        sizePanel.setMaximumSize(new Dimension(1, height));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.anchor = GridBagConstraints.WEST;
        gbc.gridx = MAXGRIDX;
        gbc.gridy = row;
        panel.add(sizePanel, gbc);
    }
}
