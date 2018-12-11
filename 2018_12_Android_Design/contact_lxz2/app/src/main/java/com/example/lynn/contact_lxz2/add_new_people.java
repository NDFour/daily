package com.example.lynn.contact_lxz2;

/*
添加新联系人
 */
import android.content.ContentUris;
import android.content.ContentValues;
import android.net.Uri;
import android.provider.ContactsContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.provider.ContactsContract.RawContacts;
import android.provider.ContactsContract.Data;
import android.content.ContentUris;
import android.content.ContentValues;
import android.provider.ContactsContract.CommonDataKinds.Email;
import android.provider.ContactsContract.CommonDataKinds.Phone;
import android.provider.ContactsContract.CommonDataKinds.StructuredName;


public class add_new_people extends AppCompatActivity implements View.OnClickListener {

    private EditText ed_new_name;
    private EditText ed_new_number;
    private Button add_new_people;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_new_people);

        initWidgets();
    }

    public void initWidgets() {
        ed_new_name = (EditText) findViewById(R.id.ed_new_name);
        ed_new_number = (EditText) findViewById(R.id.ed_new_number);

        add_new_people = (Button) findViewById(R.id.add_new_people);

        add_new_people.setOnClickListener(this);
    }

    public void new_people() {
        addContact(ed_new_name.getText().toString(), ed_new_number.getText().toString());
        Toast.makeText(this, "添加联系人成功！", Toast.LENGTH_SHORT).show();
        finish();
    }

    // 一个添加联系人信息的例子
    public void addContact(String name, String phoneNumber) {
        // 创建一个空的ContentValues
        ContentValues values = new ContentValues();

        // 向RawContacts.CONTENT_URI空值插入，
        // 先获取Android系统返回的rawContactId
        // 后面要基于此id插入值
        Uri rawContactUri = getContentResolver().insert(ContactsContract.RawContacts.CONTENT_URI, values);
        long rawContactId = ContentUris.parseId(rawContactUri);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        // 内容类型
        values.put(Data.MIMETYPE, StructuredName.CONTENT_ITEM_TYPE);
        // 联系人名字
        values.put(StructuredName.GIVEN_NAME, name);
        // 向联系人URI添加联系人名字
        getContentResolver().insert(Data.CONTENT_URI, values);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        values.put(Data.MIMETYPE, Phone.CONTENT_ITEM_TYPE);
        // 联系人的电话号码
        values.put(Phone.NUMBER, phoneNumber);
        // 电话类型
        values.put(Phone.TYPE, Phone.TYPE_MOBILE);
        // 向联系人电话号码URI添加电话号码
        getContentResolver().insert(Data.CONTENT_URI, values);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        values.put(Data.MIMETYPE, Email.CONTENT_ITEM_TYPE);
        // 联系人的Email地址
        values.put(Email.DATA, "androidxx@foxmail.com");
        // 电子邮件的类型
        values.put(Email.TYPE, Email.TYPE_WORK);
        // 向联系人Email URI添加Email数据
        getContentResolver().insert(Data.CONTENT_URI, values);

        Toast.makeText(this, "联系人数据添加成功", Toast.LENGTH_SHORT).show();
    }


    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.add_new_people:
                new_people();
                break;
            default:
                Toast.makeText(this, "default...", Toast.LENGTH_SHORT).show();
        }
    }
}
