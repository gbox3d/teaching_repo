package com.example.studentcard

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
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

        // 2. 버튼을 누를 때마다 숫자를 바꾼다.
        var count = 0
        val countText = findViewById<TextView>(R.id.countText)
        val plusButton = findViewById<Button>(R.id.plusButton)
        val minusButton = findViewById<Button>(R.id.minusButton)
        val resetButton = findViewById<Button>(R.id.resetButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
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
}
