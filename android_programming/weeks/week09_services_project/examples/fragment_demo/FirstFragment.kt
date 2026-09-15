package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 1일차: Activity 안에 끼우는 화면 조각. 자기 layout(fragment_first.xml)을 가진다.
class FirstFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 1일차).
    //    Activity의 setContentView 대신 이 함수가 화면을 정한다.
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "FirstFragment onCreateView")
        return inflater.inflate(R.layout.fragment_first, container, false)
    }
}
