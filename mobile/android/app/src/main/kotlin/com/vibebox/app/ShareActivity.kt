package com.vibebox.app

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class ShareActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        when {
            intent?.action == Intent.ACTION_SEND -> {
                if (intent.type == "text/plain") {
                    handleTextShare(intent)
                }
            }
        }
        
        finish()
    }
    
    private fun handleTextShare(intent: Intent) {
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
        if (sharedText != null) {
            saveToVibeBox(sharedText)
        }
    }
    
    private fun saveToVibeBox(url: String) {
        val sharedPref = getSharedPreferences("vibebox_shared", Context.MODE_PRIVATE)
        val pendingItems = sharedPref.getStringSet("pendingItems", mutableSetOf()) ?: mutableSetOf()
        
        pendingItems.add(url)
        
        with(sharedPref.edit()) {
            putStringSet("pendingItems", pendingItems)
            apply()
        }
        
        Toast.makeText(this, "已保存到 VibeBox", Toast.LENGTH_SHORT).show()
    }
}
