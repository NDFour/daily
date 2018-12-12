package com.example.lynn.contact_lxz2;

import android.Manifest;
import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.Image;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;
import android.provider.ContactsContract.Data;

import java.io.ByteArrayOutputStream;

import static android.app.Activity.RESULT_OK;

public class f_add_new extends Fragment implements View.OnClickListener {
    // people
    private people people = null;

    // Bitmap
    private Bitmap bitmap = null;

    // EditText
    private EditText ed_new_name;
    private EditText ed_new_number;
    private EditText ed_new_email;

    // Button
    private ImageButton add_new_ok;
    private ImageButton add_new_delete;

    // ImageView
    // 联系人头像
    private ImageView new_header;

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

        // ImageView
        // 联系人头像
        new_header = (ImageView) view.findViewById(R.id.f_add_new_imgview);

        // if people != null
        if (people != null) {
            ed_new_name.setText(people.getName());
            ed_new_number.setText(people.getNumber());
            ed_new_email.setText(people.getEmailAddress());
            new_header.setImageBitmap(people.getIcon());
        }

        // Click Listener
        add_new_ok.setOnClickListener(this);
        add_new_delete.setOnClickListener(this);
        // 点击修改头像
        new_header.setOnClickListener(this);
    }

    public void new_people() {
        addContact(
                ed_new_name.getText().toString().trim(),
                ed_new_number.getText().toString().trim(),
                ed_new_email.getText().toString().trim(),
                bitmap // 联系人头像
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
                    ed_new_email.getText().toString().trim(),
                    bitmap); // 联系人头像
            Toast.makeText(getContext(), "更新联系人信息成功!", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(getContext(), "更新联系人信息失败...(删除失败)", Toast.LENGTH_SHORT).show();
        }
    }

    // 一个添加联系人信息的例子
    public void addContact(String name, String phoneNumber, String email, Bitmap header_icon) {
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

        // 插入图片
        insertPic(rawContactId);

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
            case R.id.f_add_new_imgview:
                changeHeadIcon();
                break;
            default:
                Toast.makeText(getActivity(), "default...", Toast.LENGTH_SHORT).show();
        }
    }

    // 更换联系人头像
    public void changeHeadIcon() {
        Log.i("f_add_new", "进入 changeHeadIcon");
        // 运行时权限申请
        if (ContextCompat.checkSelfPermission(getActivity(), Manifest.permission.WRITE_EXTERNAL_STORAGE) !=
                PackageManager.PERMISSION_GRANTED) {
            Log.i("f_add_new", "开始申请权限");
            // anroid 6.0
            ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
            Log.i("f_add_new", "申请权限结束");
        } else {
            // 选择图片并显示到 ImageView
            openAlbum();
            // 更改到通讯录
//            insertPic();
        }
    }

    // 打开相册
    public void openAlbum() {
        Log.i("f_add_new", "进入 openAlbum");
        Intent intent = new Intent("android.intent.action.GET_CONTENT");
        intent.setType("image/*");
        startActivityForResult(intent, 1);
    }

    // 判断权限 回调
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        Log.i("f_add_new", "申请权限回调");
        switch (requestCode) {
            case 1:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    openAlbum();
                } else {
                    Toast.makeText(getActivity(), "您拒绝了权限申请！", Toast.LENGTH_SHORT).show();
                }
                break;
            default:
        }
    }

    // 数据回传 回调
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        Log.i("f_add_new", "数据回传回调");
        switch (requestCode) {
            case 1:
                if (resultCode == RESULT_OK) {
                    //判断手机系统版本号
                    if (Build.VERSION.SDK_INT >= 19) {
                        // 4.4 及以上系统使用这个方法处理图片
                        handleImageOnKitKat(data);
                    } else {
                        // 4.4 及以下系统使用这个方法处理图片
                        handleImageBeforeKitKat(data);
                    }
                }
                break;
            default:
                break;
        }

    }

    @TargetApi(19)
    private void handleImageOnKitKat(Intent data) {
        String imagePath = null;
        Uri uri = data.getData();
        if (DocumentsContract.isDocumentUri(getActivity(), uri)) {
            // 如果是 document 类型的 Uri , 通过 document id 处理
            String docId = DocumentsContract.getDocumentId(uri);
            if ("com.android.providers.media.documents".equals(uri.getAuthority())) {
                String id = docId.split(":")[1]; // 解析出数字格式的 id
                String selection = MediaStore.Images.Media._ID + "+" + id;
                imagePath = getImagePath(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, selection);
            } else if ("com.android.providers.downloads.documents".equals(uri.getAuthority())) {
                Uri contentUri = ContentUris.withAppendedId(Uri.parse("content://downloads/public_download"), Long.valueOf(docId));
                imagePath = getImagePath(contentUri, null);
            }
        } else if ("content".equalsIgnoreCase(uri.getScheme())) {
            // 如果是 content 类型的 Uri , 则使用普通方式
            imagePath = getImagePath(uri, null);
        } else if ("file".equalsIgnoreCase(uri.getScheme())) {
            // 如果是 file 类型的 Uri, 直接获取图片路径
            imagePath = uri.getPath();
        }
        // 根据图片路径显示图
        displayImage(imagePath);
    }

    private void handleImageBeforeKitKat(Intent data) {
        Log.i("f_add_new", "进入 handleImageBeforeKitKat");
        Uri uri = data.getData();
        String imagePath = getImagePath(uri, null);
        displayImage(imagePath);
    }

    private String getImagePath(Uri uri, String selection) {
        Log.i("f_add_new", "进入 getImagePath");
        String path = null;
        // 通过 Uri 和 selection 来获取真是的图片路径
        Cursor cursor = getActivity().getContentResolver().query(uri, null, selection, null, null);
        if (cursor != null) {
            if (cursor.moveToFirst()) {
                path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
            }
            cursor.close();
        }
        return path;
    }

    private void displayImage(String imagePath) {
        Log.i("f_add_new", "进入 displayImage");
        if (imagePath != null) {
            bitmap = BitmapFactory.decodeFile(imagePath);
            // set Bitmap
            new_header.setImageBitmap(bitmap);
        } else {
            Toast.makeText(getActivity(), "Failed to get image", Toast.LENGTH_SHORT).show();
        }
    }

    // 更改照片到通讯录
    private void insertPic(long rawContactId) {
        new_header.setDrawingCacheEnabled(true);
        Bitmap people_icon = Bitmap.createBitmap(new_header.getDrawingCache());
        new_header.setDrawingCacheEnabled(false);

        ContentValues contentValues = new ContentValues();

//        Uri rawContactUri = getContext().getContentResolver().
//                insert(ContactsContract.RawContacts.CONTENT_URI, contentValues);
//        long rawContactId = ContentUris.parseId(rawContactUri);

        //往Data表入图像数据
        contentValues.clear();
        contentValues.put(Data.RAW_CONTACT_ID, rawContactId);
        contentValues.put(Data.MIMETYPE, ContactsContract.CommonDataKinds.Photo.CONTENT_ITEM_TYPE);
        ByteArrayOutputStream array = new ByteArrayOutputStream();
        people_icon.compress(Bitmap.CompressFormat.JPEG, 100, array);
        contentValues.put(ContactsContract.CommonDataKinds.Photo.PHOTO, array.toByteArray());
        getContext().getContentResolver().insert(android.provider.ContactsContract.Data.CONTENT_URI, contentValues);
    }

}
