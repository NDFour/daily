/*
 * Copyright 2005 MH-Software-Entwicklung. All rights reserved.
 * Use is subject to license terms.
 */

package com.jtattoo.demo.images;

import java.io.*;
import java.net.*;
import java.awt.*;
import javax.swing.*;

/**
 * Class to load images out of jar-files
 *
 * @author Michael Hagen
 */
public class ImageHelper {
    
    private ImageHelper() {
    }
    
    public static ImageIcon loadImage(String name) {
        ImageIcon image = null;
        try {
            URL url = ImageHelper.class.getResource(name);
            if (url != null) {
                java.awt.Image img = Toolkit.getDefaultToolkit().createImage(url);
                if (img != null)
                    image = new ImageIcon(img);
            }
        }
        catch (Throwable ex)
        { System.out.println("ERROR: loading image " + name + " failed"); }
        return image;
    }
}
