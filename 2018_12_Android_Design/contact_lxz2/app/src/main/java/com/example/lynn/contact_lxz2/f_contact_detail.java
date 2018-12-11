package com.example.lynn.contact_lxz2;

/*
联系人详情界面 (fragment)
  - 拨打电话
  - 发送短信
  - 拉黑/解除拉黑
 */

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.drawable.BitmapDrawable;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

public class f_contact_detail extends Fragment implements View.OnClickListener {

    // people
    private people people;

    // String
    // 标志当前联系人（详情页）是否已被拉黑
    private boolean isblock = false;

    // ImageView
    private ImageView img_icon = null;

    // EditText
    private EditText ed_name;
    private EditText ed_number;
    private EditText ed_mail;

    // Button
    private ImageButton btn_call;
    private ImageButton btn_message;
    private ImageButton btn_blcok;
    private ImageButton btn_edit;


    public f_contact_detail() {
        // Required empty public constructor
    }

    // 重写构造函数
    @SuppressLint("ValidFragment")
    public f_contact_detail(people people) {
        this.people = people;
    }

    // TODO: Rename and change types and number of parameters
    public static f_contact_detail newInstance(String param1, String param2) {
        f_contact_detail fragment = new f_contact_detail();
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
        View view = inflater.inflate(R.layout.f_contact_detail, container, false);

        // 初始化联系人信息页面
//        initPeople(view, people_name, people_numbler, isblock);
        initPeople(view, people.getName(), people.getNumber(), people.getEmailAddress(), people.isBlock());

        return view;
    }

    @Override
    public void onResume() {
        super.onResume();

        // Refresh the state of the +1 button each time the activity receives focus.
    }

    // TODO: Rename method, update argument and hook method into UI event

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }


    // 初始化控件 并 绑定 事件监听
    public void initPeople(View view, String name, String number, String email, boolean isblock) {
        // ImageView
        img_icon = (ImageView) view.findViewById(R.id.f_contact_detail_icon);

        // EditText
        ed_name = (EditText) view.findViewById(R.id.ed_name);
        ed_number = (EditText) view.findViewById(R.id.ed_number);
        ed_mail = (EditText) view.findViewById(R.id.ed_mail);

        // ImageButton
        btn_call = (ImageButton) view.findViewById(R.id.btn_call);
        btn_message = (ImageButton) view.findViewById(R.id.btn_message);
        btn_edit = (ImageButton) view.findViewById(R.id.btn_edit);

        // 判断联系人是否被拦截
        btn_blcok = (ImageButton) view.findViewById(R.id.btn_block);
        if (isblock) {
//            btn_blcok.setText("取消拉黑");
            btn_blcok.setBackgroundResource(R.drawable.unblock);
        }

        // ImageView
        if (people.getIcon() != null) {
//            img_icon.setImageBitmap(people.getIcon());
            img_icon.setBackground(new BitmapDrawable(people.getIcon()));
        } else {
            img_icon.setBackgroundResource(R.drawable.people_icon);
        }

        // EditText
        ed_name.setText(name);
        ed_number.setText(number);
        ed_mail.setText(email);

        // ImageButton
        btn_call.setOnClickListener(this);
        btn_message.setOnClickListener(this);
        btn_blcok.setOnClickListener(this);
        btn_edit.setOnClickListener(this);
    }

    // 按键监听
    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_call:
                Intent dialIntent = new Intent(Intent.ACTION_CALL, Uri.parse("tel:" + people.getNumber()));//直接拨打电话
                if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(getContext(), "您需要授予权限！！", Toast.LENGTH_SHORT).show();
                    ActivityCompat.requestPermissions(getActivity(), new String[]{"Manifest.permission.CALL_PHONE"}, 1);
                } else {
                    startActivity(dialIntent);
                }
                break;
            case R.id.btn_message:
                Toast.makeText(getContext(), "发送短消息", Toast.LENGTH_SHORT).show();

                //"smsto:" 后加号码为添加发送短信的联系人号码
                Uri smsToUri = Uri.parse("smsto:" + people.getNumber());
                Intent intent = new Intent(Intent.ACTION_SENDTO, smsToUri);
                //短信内容
                intent.putExtra("sms_body", "测试用~~~李刚");
                startActivity(intent);

                break;
            case R.id.btn_block:
                if (!isblock) {
                    ContactManager.changeBlock(getContext(), people.getNumber(), "yes");
                    isblock = true;
//                    btn_blcok.setText("取消拉黑");
                    btn_blcok.setBackgroundResource(R.drawable.unblock);
                    Toast.makeText(getContext(), "加入黑名单成功", Toast.LENGTH_SHORT).show();
                } else {
                    ContactManager.changeBlock(getContext(), people.getNumber(), "no");
                    isblock = false;
//                    btn_blcok.setText("拉黑");
                    btn_blcok.setBackgroundResource(R.drawable.block);
                    Toast.makeText(getContext(), "删除黑名单成功", Toast.LENGTH_SHORT).show();
                }
                break;
            case R.id.btn_edit:
                // 替换 Fragment
                FragmentTransaction transaction = getFragmentManager().beginTransaction();
                // 构造新 f_contact_detail 时传入联系人信息参数
                transaction.replace(R.id.content_view, new f_add_new(people));
                // 将替换前的 fragment 加入回退栈，按返回键时会重新显示
                transaction.addToBackStack(null);
                transaction.commitAllowingStateLoss();
                break;
            default:
                Toast.makeText(getContext(), "没有捕捉这个按钮点击事件", Toast.LENGTH_SHORT).show();
        }
    }

}

