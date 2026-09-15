package com.example.fragmentdemo

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.fragmentdemo.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. 앱을 처음 켰을 때만 빈 자리에 FirstFragment를 끼운다(9주차 1일차).
        //    회전 뒤에는 savedInstanceState가 null이 아니고, 보고 있던 조각을 시스템이 되살려 준다(3주차 복원과 같은 원리).
        //    바꾸기는 세 줄이다: 바꾸기 시작(beginTransaction) → 자리에 조각 넣기(replace) → 확정(commit).
        if (savedInstanceState == null) {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 2. [첫 번째 조각] 버튼: 빈 자리의 조각을 FirstFragment로 바꾼다. 화면(Activity)은 그대로다(9주차 1일차).
        binding.firstButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 3. [두 번째 조각] 버튼: 빈 자리의 조각을 SecondFragment로 바꾼다. commit()을 빼면 아무것도 바뀌지 않는다(9주차 1일차).
        binding.secondButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, SecondFragment())
            transaction.commit()
        }
    }
}
