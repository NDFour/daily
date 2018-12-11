package com.example.lynn.contact_lxz2;

/*
联系人详情页面 (Activity)
  - 拨打电话
  - 发送短信
  - 拉黑/解除拉黑
 */
import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class people_detail extends AppCompatActivity implements View.OnClickListener {

    private String name;
    private String number;
    private String isBlock; // yes/no
    private String position;

    private EditText ed_name;
    private EditText ed_number;

    private Button btn_call;
    private Button btn_message;
    private Button btn_blcok;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_people_detail);

        // get data from LastActivity
        Intent intent = getIntent();
        name = intent.getStringExtra("name");
        number = intent.getStringExtra("number");
        isBlock = intent.getStringExtra("isblock");
        position = intent.getStringExtra("position");

        // 初始化联系人信息页面
        initPeople(name, number, isBlock);
    }

    public void initPeople(String name, String number, String isblock) {
        ed_name = (EditText) findViewById(R.id.ed_name);
        ed_number = (EditText) findViewById(R.id.ed_number);

        btn_call = (Button) findViewById(R.id.btn_call);
        btn_message = (Button) findViewById(R.id.btn_message);

        // 判断联系人是否被拦截
        btn_blcok = (Button) findViewById(R.id.btn_block);
        if (isblock.equals("yes")) {
            btn_blcok.setText("取消拉黑");
        }

        ed_name.setText(name);
        ed_number.setText(number);

        btn_call.setOnClickListener(this);
        btn_message.setOnClickListener(this);
        btn_blcok.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_call:
                Intent dialIntent = new Intent(Intent.ACTION_CALL, Uri.parse("tel:" + number));//直接拨打电话
                if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "您需要授予权限！！", Toast.LENGTH_SHORT).show();
                    ActivityCompat.requestPermissions(people_detail.this, new String[]{"Manifest.permission.CALL_PHONE"}, 1);
                } else {
                    startActivity(dialIntent);
                }
                break;
            case R.id.btn_message:
                Toast.makeText(this, "发送短消息", Toast.LENGTH_SHORT).show();

                //"smsto:" 后加号码为添加发送短信的联系人号码
                Uri smsToUri = Uri.parse("smsto:" + number);
                Intent intent = new Intent(Intent.ACTION_SENDTO, smsToUri);
                //短信内容
                intent.putExtra("sms_body", "测试用~~~李鑫梓");
                startActivity(intent);

                break;
            case R.id.btn_block:
                if (isBlock.equals("no")) {
                    ContactManager.changeBlock(this, number, "yes");
                    isBlock = "yes";
                    btn_blcok.setText("取消拉黑");
                    Toast.makeText(this, "加入黑名单成功", Toast.LENGTH_SHORT).show();
                } else {
                    ContactManager.changeBlock(this, number, "no");
                    isBlock = "no";
                    btn_blcok.setText("拉黑");
                    Toast.makeText(this, "删除黑名单成功", Toast.LENGTH_SHORT).show();
                }
                break;
            default:
                Toast.makeText(this, "没有捕捉这个按钮点击事件", Toast.LENGTH_SHORT).show();
        }
    }

}
