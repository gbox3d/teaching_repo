package com.example.studentcard

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    // 숫자를 onCreate 밖, class 바로 안에 둔다. onCreate와 onSaveInstanceState가 함께 쓴다.
    var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("Life", "onCreate")
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. id로 TextView를 찾아 글자를 바꾼다.
        val name = "홍길동"
        val nameText = findViewById<TextView>(R.id.nameText)
        nameText.text = "이름: $name"

        // 2. 저장해 둔 숫자가 있으면 꺼내 쓰고, 없으면(처음 실행) 0으로 시작한다.
        count = savedInstanceState?.getInt("count") ?: 0
        val countText = findViewById<TextView>(R.id.countText)
        countText.text = "$count"

        // 3. 버튼을 누를 때마다 숫자를 바꾼다. +1은 Toast로도 알린다.
        val plusButton = findViewById<Button>(R.id.plusButton)
        val minusButton = findViewById<Button>(R.id.minusButton)
        val resetButton = findViewById<Button>(R.id.resetButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
            Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
        }

        minusButton.setOnClickListener {
            count = count - 1
            countText.text = "$count"
        }

        resetButton.setOnClickListener {
            count = 0
            countText.text = "$count"
        }
    }

    // 4. 화면이 사라지기 전에 시스템이 부른다. 여기서 숫자를 저장한다.
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("count", count)
        Log.d("Life", "onSaveInstanceState count=$count")
    }

    // 5. 나머지 생명주기 콜백. 불릴 때마다 Logcat에 이름을 남긴다.
    override fun onStart() {
        super.onStart()
        Log.d("Life", "onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d("Life", "onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d("Life", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d("Life", "onStop")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("Life", "onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("Life", "onDestroy")
    }
}
