package com.example.lynn.contact_lxz2;

import android.annotation.SuppressLint;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;
import android.provider.ContactsContract.Data;

public class f_add_new extends Fragment implements View.OnClickListener {
    // people
    private people people = null;

    // EditText
    private EditText ed_new_name;
    private EditText ed_new_number;
    private EditText ed_new_email;

    // Button
    private ImageButton add_new_ok;
    private ImageButton add_new_delete;

    public f_add_new() {
        // Required empty public constructor
    }

    // 重写构造函数
    @SuppressLint("ValidFragment")
    public f_add_new(people people) {
        this.people = people;
    }

    // TODO: Rename and change types and number of parameters
    public static f_add_new newInstance(String param1, String param2) {
        f_add_new fragment = new f_add_new();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.f_add_new, container, false);

        // 初始化控件
        initWidgets(view);

        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }


    public void initWidgets(View view) {
        // EditText
        ed_new_name = (EditText) view.findViewById(R.id.ed_new_name);
        ed_new_number = (EditText) view.findViewById(R.id.ed_new_number);
        ed_new_email = (EditText) view.findViewById(R.id.ed_new_email);

        // Button
        add_new_ok = (ImageButton) view.findViewById(R.id.add_new_ok);
        add_new_delete = (ImageButton) view.findViewById(R.id.add_new_delete);

        // if people != null
        if (people != null) {
            ed_new_name.setText(people.getName());
            ed_new_number.setText(people.getNumber());
            ed_new_email.setText(people.getEmailAddress());
        }

        // Click Listener
        add_new_ok.setOnClickListener(this);
        add_new_delete.setOnClickListener(this);
    }

    public void new_people() {
        addContact(
                ed_new_name.getText().toString().trim(),
                ed_new_number.getText().toString().trim(),
                ed_new_email.getText().toString().trim()
        );
        Toast.makeText(getActivity(), "添加联系人成功！", Toast.LENGTH_SHORT).show();
    }

    // 更新联系人信息
    public void updateContact() {
        // 先删除原来的联系人，之后新建
        String rawid = people.getRawId();
        if (ContactManager.delaPeople(getContext(), rawid)) {
            // 关闭当前 fragment
            getFragmentManager().popBackStack();

            // 新建联系人
            addContact(
                    ed_new_name.getText().toString().trim(),
                    ed_new_number.getText().toString().trim(),
                    ed_new_email.getText().toString().trim());
            Toast.makeText(getContext(), "更新联系人信息成功!", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(getContext(), "更新联系人信息失败...(删除失败)", Toast.LENGTH_SHORT).show();
        }
    }

    // 一个添加联系人信息的例子
    public void addContact(String name, String phoneNumber, String email) {
        // 创建一个空的ContentValues
        ContentValues values = new ContentValues();

        // 向RawContacts.CONTENT_URI空值插入，
        // 先获取Android系统返回的rawContactId
        // 后面要基于此id插入值
        Uri rawContactUri = getActivity().getContentResolver().insert(ContactsContract.RawContacts.CONTENT_URI, values);
        long rawContactId = ContentUris.parseId(rawContactUri);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        // 内容类型
        values.put(Data.MIMETYPE, ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE);
        // 联系人名字
        values.put(ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME, name);
        // 向联系人URI添加联系人名字
        getActivity().getContentResolver().insert(Data.CONTENT_URI, values);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        values.put(Data.MIMETYPE, ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE);
        // 联系人的电话号码
        values.put(ContactsContract.CommonDataKinds.Phone.NUMBER, phoneNumber);
        // 电话类型
        values.put(ContactsContract.CommonDataKinds.Phone.TYPE, ContactsContract.CommonDataKinds.Phone.TYPE_MOBILE);
        // 向联系人电话号码URI添加电话号码
        getActivity().getContentResolver().insert(Data.CONTENT_URI, values);
        values.clear();

        values.put(Data.RAW_CONTACT_ID, rawContactId);
        values.put(Data.MIMETYPE, ContactsContract.CommonDataKinds.Email.CONTENT_ITEM_TYPE);
        // 联系人的Email地址
        values.put(ContactsContract.CommonDataKinds.Email.DATA, email);
        // 电子邮件的类型
        values.put(ContactsContract.CommonDataKinds.Email.TYPE, ContactsContract.CommonDataKinds.Email.TYPE_WORK);
        // 向联系人Email URI添加Email数据
        getActivity().getContentResolver().insert(Data.CONTENT_URI, values);

        Toast.makeText(getActivity(), "联系人数据添加成功", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.add_new_ok:
                // if people != null ==> update info not create new info
                if (people != null) {
                    // 更新联系人信息
                    updateContact();
                    // 关闭当前 fragment
                    getFragmentManager().popBackStack();
                } else {
                    new_people();
                    // 关闭当前 fragment
                    getFragmentManager().popBackStack();
                }
                break;
            case R.id.add_new_delete:
//                Toast.makeText(getContext(), "删除或者取消编辑当前联系人", Toast.LENGTH_SHORT).show();
                // 新建用户
                if (people == null) {
                    Toast.makeText(getContext(), "取消新建联系人", Toast.LENGTH_SHORT).show();
                    // 关闭当前 fragment
                    getFragmentManager().popBackStack();
                } else {
                    // 删除已存在用户信息
                    String rawid = people.getRawId();
                    if (ContactManager.delaPeople(getContext(), rawid)) {
                        // 关闭当前 fragment
                        getFragmentManager().popBackStack();
                        Toast.makeText(getContext(), "删除成功!", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(getContext(), "删除失败...", Toast.LENGTH_SHORT).show();
                    }
                }
                break;
            default:
                Toast.makeText(getActivity(), "default...", Toast.LENGTH_SHORT).show();
        }
    }

}
