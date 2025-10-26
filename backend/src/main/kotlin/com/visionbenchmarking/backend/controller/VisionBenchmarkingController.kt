package com.visionbenchmarking.backend

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile


@RestController
@RequestMapping("/api")
@CrossOrigin(origins = ["http://cv-benchmark-frontend.s3-website.us-east-2.amazonaws.com"])
class VisionBenchMarkingController {
    @PostMapping("/run-inference", consumes=["multipart/form-data"])
    fun runInference(@RequestPart("file") file: MultipartFile): ResponseEntity<Map<String, Any>> {
        val response = mapOf(
            "processing_time_ms" to 123,
            "objects_detected" to 0,
            "annotated_img_url" to "https://lmfao.png"
        )

        return ResponseEntity.ok(response)
    }

    @GetMapping("/")
    fun test(): ResponseEntity<String> {
        return ResponseEntity.ok("home")
    }
}