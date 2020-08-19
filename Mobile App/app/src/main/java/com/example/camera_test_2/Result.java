package com.example.camera_test_2;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class Result extends AppCompatActivity {

    ImageView imageView;
    EditText numberView;
    Button searchBtn;
    Button backBtn;

    String number;
    String image;

    ProgressDialog progressDialog;

        String urll = "https://husseinalshaikhaaaaaa.pythonanywhere.com/search-item";
//    String urll = "https://webhook.site/c291ca6e-5b7b-4bf5-afda-d1e04cc6c6e6";

    private String readStream(InputStream is) throws IOException {
        StringBuilder sb = new StringBuilder();
        BufferedReader r = new BufferedReader(new InputStreamReader(is), 1000);
        for (String line = r.readLine(); line != null; line = r.readLine()) {
            sb.append(line);
        }
        System.out.println("---------------------------------"+sb);
        is.close();
        return sb.toString();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        imageView = findViewById(R.id.imageView);
        numberView = findViewById(R.id.numberView);
        searchBtn = findViewById(R.id.Search);
        backBtn = findViewById(R.id.Back);

        Intent intent = getIntent();
        number = intent.getStringExtra("number");
        image = intent.getStringExtra("image");

        numberView.setText(number);

        byte[] decodedString = Base64.decode(image, Base64.DEFAULT);
        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        imageView.setImageBitmap(decodedByte);

        searchBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RetrieveFeedTask retrieveFeedTask = new RetrieveFeedTask();
                retrieveFeedTask.execute();
            }
        });

        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(Result.this, MainActivity.class);
                startActivity(intent);

            }
        });

    }

    class RetrieveFeedTask extends AsyncTask<String, String, String> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

            progressDialog = ProgressDialog.show(Result.this, "Searching in Database", "Please Wait", false, false);
        }

        @SuppressLint("ShowToast")
        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);

            progressDialog.dismiss();
            System.out.println(s);
            Toast.makeText(Result.this, s, Toast.LENGTH_LONG).show();

        }

        @SuppressLint("WrongThread")
        @Override
        protected String doInBackground(String... strings) {
            URL url = null;
            HttpURLConnection client = null;
            String msg = "Car NOT Found";

            try {
                url = new URL(urll);
                client = (HttpURLConnection) url.openConnection();

                client.setRequestMethod("POST");
//                client.setRequestProperty("Key", "Value");
                client.setDoInput(true);
                client.setDoOutput(true);

                OutputStreamWriter out = new OutputStreamWriter(
                        client.getOutputStream());

                out.write("data=" + numberView.getText().toString()+","+number);
                out.close();

                BufferedReader in = new BufferedReader(
                        new InputStreamReader(
                                client.getInputStream()));
                String decodedString;
                while ((decodedString = in.readLine()) != null) {
                    if(decodedString.equals("True")){
                        msg = "Car Found";
                        break;
                    }
                }
                in.close();

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (client != null) // Make sure the connection is not null.
                    client.disconnect();
            }
            return msg;
        }
    }
}