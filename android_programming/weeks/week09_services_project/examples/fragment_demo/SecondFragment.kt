package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 1일차: 두 번째 화면 조각. FirstFragment와 모양이 같고 layout만 다르다(fragment_second.xml).
class SecondFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 1일차).
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "SecondFragment onCreateView")
        return inflater.inflate(R.layout.fragment_second, container, false)
    }
}
