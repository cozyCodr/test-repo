"use client";

import React, { useState, useCallback } from "react";
import { AlertCircle, Upload, X } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useRouter } from "next/navigation";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB in bytes
const MAX_FILES = 5;
const ALLOWED_TYPES = [
	"application/pdf",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	"application/vnd.openxmlformats-officedocument.presentationml.presentation",
	"image/jpeg",
	"image/png",
	"image/gif",
	"image/webp",
];

const ALLOWED_EXTENSIONS = [
	".pdf",
	".docx",
	".pptx",
	".jpg",
	".jpeg",
	".png",
	".gif",
	".webp",
];

const UploadMaterialsPage = () => {
	const router = useRouter();
	const [files, setFiles] = useState([]);
	const [dragActive, setDragActive] = useState(false);
	const [error, setError] = useState("");
	const [uploading, setUploading] = useState(false);
	const [previews, setPreviews] = useState({});

	const validateFile = (file: any) => {
		if (!ALLOWED_TYPES.includes(file.type)) {
			throw new Error(
				`File type ${file.type} is not supported. Please upload PDF, DOCX, PPTX, or image files only.`
			);
		}
		if (file.size > MAX_FILE_SIZE) {
			throw new Error(`File ${file.name} is too large. Maximum size is 10MB.`);
		}
	};

	const generatePreview = async (file: any) => {
		if (file.type.startsWith("image/")) {
			return new Promise((resolve) => {
				const reader = new FileReader();
				reader.onloadend = () => resolve(reader.result);
				reader.readAsDataURL(file);
			});
		}
		return null;
	};

	const handleNavigation = useCallback(
		(path) => {
			if (files.length === 0) {
				setError("Please upload at least one file before proceeding.");
				return;
			}

			try {
				const fileData = files.map((file) => ({
					name: file?.name,
					size: file.size,
					type: file.type,
					preview: previews[file.name] || null,
				}));
				localStorage.setItem("uploadedFiles", JSON.stringify(fileData));
				router.push(path);
			} catch (err) {
				setError("Error processing files. Please try again.");
				console.error("Navigation error:", err);
			}
		},
		[files, previews, router]
	);

	const handleDrag = useCallback((e) => {
		e.preventDefault();
		e.stopPropagation();
		if (e.type === "dragenter" || e.type === "dragover") {
			setDragActive(true);
		} else if (e.type === "dragleave") {
			setDragActive(false);
		}
	}, []);

	const processFiles = useCallback(
		async (fileList) => {
			setError("");

			if (files.length >= MAX_FILES) {
				setError(`Maximum ${MAX_FILES} files allowed.`);
				return;
			}

			const remainingSlots = MAX_FILES - files.length;
			const filesToAdd = Array.from(fileList).slice(0, remainingSlots);

			try {
				setUploading(true);
				filesToAdd.forEach(validateFile);

				const newPreviews = {};
				await Promise.all(
					filesToAdd.map(async (file) => {
						const preview = await generatePreview(file);
						if (preview) {
							newPreviews[file.name] = preview;
						}
					})
				);

				await Promise.all(
					filesToAdd.map(async (file) => {
						await new Promise((resolve) => setTimeout(resolve, 1000));
						return file;
					})
				);

				setPreviews((prev) => ({ ...prev, ...newPreviews }));
				setFiles((prevFiles) => [...prevFiles, ...filesToAdd]);
			} catch (err) {
				setError(err.message);
			} finally {
				setUploading(false);
			}
		},
		[files]
	);

	const handleDrop = useCallback(
		(e) => {
			e.preventDefault();
			e.stopPropagation();
			setDragActive(false);

			if (e.dataTransfer.files && e.dataTransfer.files[0]) {
				processFiles(e.dataTransfer.files);
			}
		},
		[processFiles]
	);

	const handleFileInput = useCallback(
		(e) => {
			if (e.target.files) {
				processFiles(e.target.files);
			}
		},
		[processFiles]
	);

	const removeFile = useCallback((index) => {
		setFiles((prevFiles) => {
			const fileToRemove = prevFiles[index];
			const newFiles = prevFiles.filter((_, i) => i !== index);

			setPreviews((prev) => {
				const newPreviews = { ...prev };
				delete newPreviews[fileToRemove.name];
				return newPreviews;
			});

			return newFiles;
		});
		setError("");
	}, []);

	const getFileIcon = useCallback(
		(file) => {
			if (file.type.startsWith("image/")) {
				return previews[file.name] ? (
					<img
						src={previews[file.name]}
						alt={file.name}
						className="w-12 h-12 object-cover rounded"
					/>
				) : (
					<div className="w-5 h-5 text-purple-400">📷</div>
				);
			}

			const extension = file.name.split(".").pop().toLowerCase();
			switch (extension) {
				case "pdf":
					return <div className="w-5 h-5 text-red-400">📄</div>;
				case "docx":
					return <div className="w-5 h-5 text-blue-400">📝</div>;
				case "pptx":
					return <div className="w-5 h-5 text-orange-400">📊</div>;
				default:
					return <div className="w-5 h-5 text-gray-400">📄</div>;
			}
		},
		[previews]
	);

	const navigationButtons = [
		{
			title: "Generate Questions",
			icon: "📚",
			path: "/team",
			description: "Create a quiz from your materials",
		},
		{
			title: "Ask Questions",
			icon: "💭",
			path: "/chat",
			description: "Chat with AI about your content",
		},
		{
			title: "Extract Key Concepts",
			icon: "🧠",
			path: "/key-concepts",
			description: "Identify main ideas and themes",
		},
	];

	return (
		<div className="max-w-4xl mx-auto p-8">
			<h1 className="text-3xl font-bold text-center mb-8">
				Upload Learning Materials
			</h1>

			{error && (
				<Alert variant="destructive" className="mb-6">
					<AlertCircle className="h-4 w-4" />
					<AlertDescription>{error}</AlertDescription>
				</Alert>
			)}

			<div
				className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300"
					} ${uploading ? "opacity-50 cursor-not-allowed" : ""}`}
				onDragEnter={handleDrag}
				onDragLeave={handleDrag}
				onDragOver={handleDrag}
				onDrop={handleDrop}
			>
				<div className="flex flex-col items-center gap-4">
					<Upload
						className={`w-12 h-12 ${dragActive ? "text-blue-500" : "text-gray-400"
							}`}
					/>
					<div>
						<p className="text-lg">
							Drag and drop your files here, or{" "}
							<label
								className={`${uploading
										? "text-gray-400"
										: "text-blue-500 hover:text-blue-600"
									} cursor-pointer`}
							>
								browse
								<input
									type="file"
									className="hidden"
									multiple
									onChange={handleFileInput}
									disabled={uploading}
									accept={ALLOWED_EXTENSIONS.join(",")}
								/>
							</label>
						</p>
						<p className="text-sm text-gray-500 mt-2">
							PDF, DOCX, PPTX, or images up to 10MB each (Maximum {MAX_FILES}{" "}
							files)
						</p>
					</div>
				</div>
			</div>

			{files.length > 0 && (
				<div className="mt-8">
					<h2 className="text-xl font-semibold mb-4">
						Uploaded Files ({files.length}/{MAX_FILES})
					</h2>
					<div className="max-h-60 overflow-y-auto border rounded-lg mb-8">
						{files.map((file, index) => (
							<div
								key={index}
								className="flex items-center justify-between p-4 border-b last:border-b-0 hover:bg-gray-50"
							>
								<div className="flex items-center gap-3">
									{getFileIcon(file)}
									<div className="flex flex-col">
										<span className="truncate font-medium">{file.name}</span>
										<span className="text-sm text-gray-500">
											{(file.size / (1024 * 1024)).toFixed(2)} MB
										</span>
									</div>
								</div>
								<button
									onClick={() => removeFile(index)}
									className="text-gray-500 hover:text-red-500 transition-colors"
									disabled={uploading}
								>
									<X className="w-5 h-5" />
								</button>
							</div>
						))}
					</div>
				</div>
			)}

			<div className="mt-8 space-y-4">
				{navigationButtons.map((button, index) => (
					<button
						key={index}
						onClick={() => handleNavigation(button.path)}
						className={`w-full bg-white border-2 border-gray-200 p-4 rounded-lg flex items-center gap-4 transition-all ${files.length === 0
								? "opacity-50 cursor-not-allowed"
								: "hover:border-gray-300 hover:shadow-md"
							}`}
						disabled={files.length === 0}
					>
						<div className="flex items-center justify-center w-12 h-12 rounded-full bg-gray-100">
							<span className="text-2xl">{button.icon}</span>
						</div>
						<div className="text-left">
							<div className="font-semibold text-lg">{button.title}</div>
							<div className="text-sm text-gray-500">{button.description}</div>
						</div>
					</button>
				))}
			</div>
		</div>
	);
};

export default UploadMaterialsPage;
