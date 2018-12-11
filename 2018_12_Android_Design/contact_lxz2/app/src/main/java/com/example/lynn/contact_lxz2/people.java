package com.example.lynn.contact_lxz2;

/*
联系人对象类
 */

import android.graphics.Bitmap;

public class people {
    private String name;
    private String number;
    private boolean block; // 是否拦截
    private Bitmap icon; // 头像
    private String rawId = null; // rawId 用于删除联系人
    private String emailAddress = null; // email Address

    public people(String name, String number, Boolean block, Bitmap head_icon, String rawId, String emailAddress) {
        this.name = name;
        this.number = number;
        this.block = block;
        this.icon = head_icon;
        this.rawId = rawId;
        this.emailAddress = emailAddress;
    }

    public String getName() {
        return name;
    }

    public String getNumber() {
        return number;
    }

    public Bitmap getIcon() {
        return icon;
    }

    public String getRawId() {
        return rawId;
    }

    public String getEmailAddress() {
        return emailAddress;
    }

    public boolean isBlock() {
        return block;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public void setBlock(Boolean block) {
        this.block = block;
    }
}
