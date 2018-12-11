package com.example.lynn.contact_lxz2;

import android.annotation.SuppressLint;
import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import com.google.android.gms.plus.PlusOneButton;

/**
 * A fragment with a Google +1 button.
 * Activities that contain this fragment must implement the
 * {@link fragment_black_list.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link fragment_black_list#newInstance} factory method to
 * create an instance of this fragment.
 */
public class fragment_black_list extends Fragment {
    private ListView lv_black;
    private people[] contact_arr;

    public fragment_black_list() {
        // Required empty public constructor
    }

    // TODO: Rename and change types and number of parameters
    public static fragment_black_list newInstance(String param1, String param2) {
        fragment_black_list fragment = new fragment_black_list();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @SuppressLint("LongLogTag")
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_fragment_black_list, container, false);

//        contact_arr = null;

        lv_black = view.findViewById(R.id.lv_black);
        Log.i("fragment_black_list lv_back:", String.valueOf(lv_black));
        if (lv_black != null) {
            // 获取 people 对象的数组（联系人列表）
            contact_arr = ContactManager.getContact(getContext());
            people[] p_black = getBlockList(contact_arr);
            ArrayAdapter arrayAdapter = new ArrayAdapter(getContext(), android.R.layout.simple_list_item_1, ContactManager.nameToString(p_black));
            if (arrayAdapter != null) {
                lv_black.setAdapter(arrayAdapter);
            }
//        lv_black.setOnItemClickListener(new AdapterView.OnItemClickListener() {
        }

        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    // TODO: Rename method, update argument and hook method into UI event
    public void onButtonPressed(Uri uri) {
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        Log.i("fragment_black_list", "onAttach");
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }

    // 从所有联系人列表中返回需要拦截的
    public people[] getBlockList(people[] peo) {
        int for_cnt = 0;
        for (people p : peo) {
            Log.i("f_black_list getBlock()", "正在循环 peo..." + p.getNumber());
            if (ContactManager.getBlockState(getContext(), p.getNumber()).equals("yes")) {
                for_cnt++;
            }
        }

        people[] black_list = new people[for_cnt];
        for_cnt = 0;
        for (people p : peo) {
            Log.i("f_black_list getBlock()", "正在循环 peo..." + p.getNumber());
            if (ContactManager.getBlockState(getContext(), p.getNumber()).equals("yes")) {
                Log.i("f_black_list getBlock()", "找到一个" + p.getNumber());
                black_list[for_cnt] = p;
                for_cnt++;
            }
        }

        if (for_cnt == 0) {
            Log.i("f_black_list getBlock()", "没有找到一个黑名单联系人");
            return new people[]{};
        }
        Log.i("f_black_list", String.valueOf(black_list.length));
        return black_list;
    }

}
