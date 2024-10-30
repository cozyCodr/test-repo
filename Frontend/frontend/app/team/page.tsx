"use client";

import React, { useState } from "react";
import { ChevronRight, CheckCircle, XCircle } from "lucide-react";

interface Question {
	id: number;
	question: string;
	options: string[];
	correctAnswer: number;
}

const QuizPage = () => {
	const [selectedCourse, setSelectedCourse] = useState("");
	const [selectedTopic, setSelectedTopic] = useState("");
	const [currentQuestion, setCurrentQuestion] = useState<number | null>(null);
	const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
	const [isAnswered, setIsAnswered] = useState(false);

	//Array of objects for courses
	const courses = ["Physics"];
	const topics = {
		Physics: ["Waves", "Capacitance", "Optics", "Electrostatics"],
	};

	const sampleQuestions: Question[] = [
		{
			id: 1,
			question: "What is the primary function of mitochondria in a cell?",
			options: [
				"Protein synthesis",
				"Energy production",
				"Water storage",
				"Cell division",
			],
			correctAnswer: 1,
		},
		{
			id: 2,
			question: "Which of the following is a noble gas?",
			options: ["Oxygen", "Nitrogen", "Helium", "Chlorine"],
			correctAnswer: 2,
		},
	];

	const handleStartQuiz = () => {
		setCurrentQuestion(0);
		setSelectedAnswer(null);
		setIsAnswered(false);
	};

	const handleAnswerSubmit = () => {
		if (selectedAnswer !== null) {
			setIsAnswered(true);
		}
	};

	const handleNextQuestion = () => {
		if (
			currentQuestion !== null &&
			currentQuestion < sampleQuestions.length - 1
		) {
			setCurrentQuestion(currentQuestion + 1);
			setSelectedAnswer(null);
			setIsAnswered(false);
		}
	};

	return (
		<div className="p-6 max-w-6xl mx-auto">
			<div className="bg-white rounded-lg shadow-sm p-6">
				<h2 className="text-2xl font-semibold mb-6">Quiz</h2>

				{currentQuestion === null ? (
					<div className="space-y-6">
						<div className="grid grid-cols-2 gap-6">
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Select Course
								</label>
								<select
									value={selectedCourse}
									onChange={(e) => {
										setSelectedCourse(e.target.value);
										setSelectedTopic("");
									}}
									className="w-full border rounded-lg px-3 py-2"
								>
									<option value="">Select a course...</option>
									{courses.map((course) => (
										<option key={course} value={course}>
											{course}
										</option>
									))}
								</select>
							</div>
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Select Topic
								</label>
								<select
									value={selectedTopic}
									onChange={(e) => setSelectedTopic(e.target.value)}
									className="w-full border rounded-lg px-3 py-2"
									disabled={!selectedCourse}
								>
									<option value="">Select a topic...</option>
									{selectedCourse &&
										topics[selectedCourse as keyof typeof topics].map(
											(topic) => (
												<option key={topic} value={topic}>
													{topic}
												</option>
											)
										)}
								</select>
							</div>
						</div>
						<button
							onClick={handleStartQuiz}
							disabled={!selectedCourse || !selectedTopic}
							className="bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
						>
							Start Quiz
						</button>
					</div>
				) : (
					<div>
						<div className="mb-8">
							<div className="text-sm text-gray-500 mb-2">
								Question {currentQuestion + 1} of {sampleQuestions.length}
							</div>
							<h3 className="text-lg font-medium">
								{sampleQuestions[currentQuestion].question}
							</h3>
						</div>

						<div className="space-y-3">
							{sampleQuestions[currentQuestion].options.map((option, index) => (
								<div
									key={index}
									onClick={() => !isAnswered && setSelectedAnswer(index)}
									className={`p-4 rounded-lg border cursor-pointer
                    ${
											selectedAnswer === index
												? isAnswered
													? index ===
													  sampleQuestions[currentQuestion].correctAnswer
														? "border-green-500 bg-green-50"
														: "border-red-500 bg-red-50"
													: "border-blue-500 bg-blue-50"
												: "border-gray-200 hover:bg-gray-50"
										}
                  `}
								>
									<div className="flex items-center justify-between">
										<span>{option}</span>
										{isAnswered &&
											selectedAnswer === index &&
											(index ===
											sampleQuestions[currentQuestion].correctAnswer ? (
												<CheckCircle className="text-green-500" size={20} />
											) : (
												<XCircle className="text-red-500" size={20} />
											))}
									</div>
								</div>
							))}
						</div>

						<div className="mt-6 flex justify-between">
							{!isAnswered ? (
								<button
									onClick={handleAnswerSubmit}
									disabled={selectedAnswer === null}
									className="bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
								>
									Submit Answer
								</button>
							) : (
								<button
									onClick={handleNextQuestion}
									className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
								>
									Next Question
									<ChevronRight size={20} />
								</button>
							)}
						</div>
					</div>
				)}
			</div>
		</div>
	);
};

export default QuizPage;
