package com.example.lynn.contact_lxz2;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.media.Image;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;

import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;


public class fragment_contact_list extends Fragment implements View.OnClickListener {

    // ListView
    // 联系人ListView
    private ListView contact_list;

    // Button
    private ImageButton btn_search;

    // EditText
    private EditText ed_search;

    // 联系人对象数组
    private people[] contact_arr;

    public fragment_contact_list() {
        // Required empty public constructor
    }


    // TODO: Rename and change types and number of parameters
    public static fragment_contact_list newInstance(String param1, String param2) {
        fragment_contact_list fragment = new fragment_contact_list();
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
        View view = inflater.inflate(R.layout.fragment_fragment_contact_list, container, false);

        Log.i("fragment_contact_list", "又进入到 onCreateView 函数了");

        // 浮动按钮事件绑定
        FloatingActionButton fab = (FloatingActionButton) view.findViewById(R.id.fab_contact);
        if (fab != null) {
            fab.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Toast.makeText(getContext(), "添加新联系人...", Toast.LENGTH_SHORT).show();

                    // 替换 Fragment
                    FragmentTransaction transaction = getFragmentManager().beginTransaction();
                    // 构造新 f_contact_detail 时传入联系人信息参数
                    transaction.replace(R.id.content_view, new f_add_new());
                    // 将替换前的 fragment 加入回退栈，按返回键时会重新显示
                    transaction.addToBackStack(null);
                    transaction.commitAllowingStateLoss();

                }
            });

        }

        // 初始化 联系人列表
        initContactListView(view);

        // 初始化搜索按钮
        btn_search = (ImageButton) view.findViewById(R.id.f_contact_list_btn_search);
        btn_search.setOnClickListener(this);
        // 初始化 搜索框
        ed_search = (EditText) view.findViewById(R.id.f_contact_list_ed_search);

        return view;
    }

    public void initContactListView(View view) {
        // 获取 people 对象的数组（联系人列表）
        contact_arr = ContactManager.getContact(getContext());
//        ArrayAdapter arrayAdapter = new ArrayAdapter(getContext(), android.R.layout.simple_list_item_1, ContactManager.nameToString(contact_arr));
        MyBaseAdapter myBaseAdapter = new MyBaseAdapter();
        contact_list = (ListView) view.findViewById(R.id.contact_list);
//        contact_list.setAdapter(arrayAdapter);
        contact_list.setAdapter(myBaseAdapter);

        contact_list.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @SuppressLint("LongLogTag")
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                Toast.makeText(getContext(), "点击了第" + position, Toast.LENGTH_SHORT).show();

                // 查看本地 sp 文件中是否记录了该电话号码的 isBlock 状态
                boolean isblock = false;
                String s_state = ContactManager.getBlockState(getContext(), contact_arr[position].getNumber());
                if (s_state.equals("yes")) {
                    Log.i("fragment_contact_list", "拦截该号码");
                    isblock = true;
                    contact_arr[position].setBlock(true);
                } else {
                    Log.i("fragment_contact_list", "不拦截该号码");
                    contact_arr[position].setBlock(false);
                }

                // 替换 Fragment
                FragmentTransaction transaction = getFragmentManager().beginTransaction();
                // 构造新 f_contact_detail 时传入联系人信息参数
                transaction.replace(R.id.content_view, new f_contact_detail(contact_arr[position]));

                // 将替换前的 fragment 加入回退栈，按返回键时会重新显示
                transaction.addToBackStack(null);
                transaction.commitAllowingStateLoss();
            }
        });


    }

    @Override
    public void onResume() {
        super.onResume();
        Log.i("fragment_contact_list", "又进入到 onResume 函数了");
        // 更新联系人列表
        initContactListView(getView());
    }


    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        Log.i("fragment_contact_list", "onAttach");
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.f_contact_list_btn_search:
                if (search() == false) {
                    Toast.makeText(getContext(), "未搜索到匹配的结果。。。", Toast.LENGTH_SHORT).show();
                }
                break;
            default:
                break;
        }
    }

    // 点击搜索按钮后的动作
    public boolean search() {
        String name = ed_search.getText().toString().trim();
        // 获取联系人数组
        people[] peoObjs = ContactManager.getContact(getContext());
        // 获取联系人名字数组
        String[] peoNames = ContactManager.nameToString(peoObjs);

        for (int i = 0; i < peoNames.length; i++) {
            if (name.equals(peoNames[i])) {
                // 替换 Fragment
                FragmentTransaction transaction = getFragmentManager().beginTransaction();
                // 构造新 f_contact_detail 时传入联系人信息参数
                transaction.replace(R.id.content_view, new f_contact_detail(peoObjs[i]));
                // 将替换前的 fragment 加入回退栈，按返回键时会重新显示
                transaction.addToBackStack(null);
                transaction.commitAllowingStateLoss();

                return true;
            }
        }

        // 未找到匹配的结果
        return false;
    }

    // 重写列表适配器
    class MyBaseAdapter extends BaseAdapter {

        @Override
        public int getCount() {
            return contact_arr.length;
        }

        @Override
        public Object getItem(int position) {
            return contact_arr[position];
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @SuppressLint("LongLogTag")
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View view = View.inflate(getContext(), R.layout.f_contact_list_item, null);

            TextView tv_name = (TextView) view.findViewById(R.id.f_contact_list_item_name);
            ImageView img_icon = (ImageView) view.findViewById(R.id.f_contact_list_item_icon);

            tv_name.setText(contact_arr[position].getName());

            Bitmap icon = contact_arr[position].getIcon();
            if (icon != null) {
                Log.i("fragment_contact_list[渲染List]", "正在给"+contact_arr[position].getName()+"设置头像");
                img_icon.setImageBitmap(icon);
            }else{
                Log.i("fragment_contact_list[渲染List]", "这个没有头像==>"+contact_arr[position].getName());
            }

            return view;
        }

    }
}


