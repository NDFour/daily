package com.example.lynn.contact_lxz2;

/*
辅助类
  - 获取联系人列表
  - 修改联系人黑名单状态
  - 获取联系人黑名单状态
  - 返回联系人姓名
      接收：联系人数组
      返回：联系人姓名数组
  - 返回联系人联系方式 String
      接收：联系人数组
      返回：联系人联系方式数组
 */

import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Context;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.ContactsContract;
import android.util.Log;

import java.io.InputStream;
import java.lang.reflect.Array;
import java.util.List;

public class ContactManager {

    // get contact list from phone
    // 自定义函数，读取系统联系人，返回联系人(people)数组
    public static people[] getContact(Context context) {
        //联系人的Uri，也就是content://com.android.contacts/contacts
        Uri uri = ContactsContract.Contacts.CONTENT_URI;
        //指定获取_id和display_name两列数据，display_name即为姓名
        String[] projection = new String[]{
                ContactsContract.Contacts._ID,
                ContactsContract.Contacts.DISPLAY_NAME
        };
        //根据Uri查询相应的ContentProvider，cursor为获取到的数据集
        Cursor cursor = context.getContentResolver().query(uri, projection, null, null, null);
        people[] arr = new people[cursor.getCount()];
        int i = 0;
        if (cursor != null && cursor.moveToFirst()) {
            do {
                // rawId
                Long id = cursor.getLong(0);
                String rawId = String.valueOf(id);

                //获取姓名
                String name = cursor.getString(1);

                //指定获取NUMBER这一列数据
                String[] phoneProjection = new String[]{
                        ContactsContract.CommonDataKinds.Phone.NUMBER
                };

//                arr[i] = id + " , 姓名：" + name;

                // 获取联系人头像
                Uri pic_uri = ContentUris.withAppendedId(ContactsContract.Contacts.CONTENT_URI,
                        Long.parseLong(String.valueOf(id)));
                ContentResolver cr = context.getContentResolver();
                InputStream input = ContactsContract.Contacts.openContactPhotoInputStream(cr, pic_uri);
                Bitmap photo = null;
                if (input != null) {
                    photo = BitmapFactory.decodeStream(input);
                    Log.i("ContactManager", "该联系人设置le头像:");
                } else {
                    Log.i("ContactManager", "该联系人未设置头像:");
                }
                // 获取联系人头像结束

                //根据联系人的ID获取此人的电话号码
                Cursor phonesCusor = context.getContentResolver().query(
                        ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                        phoneProjection,
                        ContactsContract.CommonDataKinds.Phone.CONTACT_ID + "=" + id,
                        null,
                        null);
                //因为每个联系人可能有多个电话号码，所以需要遍历
                String num = null;
                if (phonesCusor != null && phonesCusor.moveToFirst()) {
                    do {
                        num = phonesCusor.getString(0);
                    } while (phonesCusor.moveToNext());
                }
                phonesCusor.close();

                // 获取邮件地址
                //查询Email类型的数据操作
                String email = "";
                Cursor emails = context.getContentResolver().query(ContactsContract.CommonDataKinds.Email.CONTENT_URI,
                        null,
                        ContactsContract.CommonDataKinds.Email.CONTACT_ID + " = " + rawId,
                        null, null);
                while (emails.moveToNext()) {
                    String emailAddress = emails.getString(emails.getColumnIndex(
                            ContactsContract.CommonDataKinds.Email.DATA));
                    email = emailAddress;
                    //添加Email的信息
/*                    sb.append(",Email=").append(emailAddress);
                    Log.e("emailAddress", emailAddress);
                    map.put("email", emailAddress);*/
                }
                emails.close();


                // 查看该号码拦截状态 yes/no
                if (ContactManager.getBlockState(context, num) == "yes") {
                    arr[i] = new people(name, num, true, photo, rawId, email);
                } else {
                    // 默认拦截状态为 false
                    arr[i] = new people(name, num, false, photo, rawId, email);
                }


                i++;
            } while (cursor.moveToNext());
        }

        cursor.close();

        return arr;
    }

    // save to sp
    // isBlock:yes/no
    public static boolean changeBlock(Context context, String number, String isBlock) {
        SharedPreferences sp = context.getSharedPreferences("data_block", Context.MODE_PRIVATE);
        SharedPreferences.Editor edit = sp.edit();

        edit.putString(number, isBlock);
        edit.commit();

        return true;
    }

    // get block state from sp
    // isBlock:yes/no
    public static String getBlockState(Context context, String number) {
        SharedPreferences sp = context.getSharedPreferences("data_block", Context.MODE_PRIVATE);
        String isBlock = sp.getString(number, "no");

        Log.i("ContactManager isBlock:", isBlock);

        return isBlock;
    }

    // 由 联系人（people）对象数组获得联系人（people）姓名数组
    public static String[] nameToString(people[] peo) {
        Log.i("fragment_contact_list", "nameToString peo.length:" + peo.length);
        if (peo.length == 0) {
            return new String[]{"空"};
        }

        String[] name = new String[peo.length];

        int p_cnt = 0;
        for (people p : peo) {
            if (p != null) {
                Log.i("xxxxxxxxxl", p.getName());
                Log.i("yyyyyyyyyl", p.getNumber());
                name[p_cnt] = p.getName();
                p_cnt++;
            } else {
                return name;
            }
        }
        return name;
    }

    // 由 联系人（people）对象数组获得联系人（people）手机号数组
    public static String[] numToString(people[] peo) {
        Log.i("fragment_contact_list", "numToString peo.length:" + peo.length);
        String[] num = new String[peo.length];

        int p_cnt = 0;
        for (people p : peo) {
            num[p_cnt] = p.getNumber();
            p_cnt++;
        }
        return num;
    }

    // 由 rawId 删除一个联系人
    public static boolean delaPeople(Context context, String rawId) {
        String where = ContactsContract.Data._ID + " =?";
        String[] whereparams = new String[]{rawId};
        int number = context.getContentResolver().delete(ContactsContract.RawContacts.CONTENT_URI, where, whereparams);
        Log.i("ContactManager", "删除了" + String.valueOf(number) + "条数据");
        if (number > 0) {
            return true;
        }
        return false;
    }


}
