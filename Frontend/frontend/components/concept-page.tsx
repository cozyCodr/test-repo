"use client";

import React, { useState } from "react";
import { Book, ChevronRight, HelpCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import Dialog from "@/components/ui/dialog";
import PdfDropzone from "./PdfDropZone";

// Types
type Concept = {
	content: string,
	explanation: string
}

const ConceptPage: React.FC = () => {
	const [isDialogOpen, setIsDialogOpen] = useState(false);
	const [selectedConcept, setSelectedConcept] = useState<Concept>({
		content: "",
		explanation: ""
	});

	const [concepts, setConcepts] = useState<Concept[]>([])


	const handleConceptClick = (concept: Concept) => {
		setSelectedConcept(concept);
		setIsDialogOpen(true);
	};

	const handleGenerateConcepts = () => {
		console.log("Generating concepts for:");
	};

	return (
		<div className="p-6 max-w-6xl mx-auto">
			<div className="bg-white rounded-lg shadow-sm p-6 mb-8">
				<h2 className="text-2xl font-semibold mb-6">Generate Key Concepts</h2>
				<div className="grid grid-cols-2 gap-6">
					<PdfDropzone concepts={concepts} setConcepts={setConcepts} />
				</div>
			</div>

			<div className="bg-white rounded-lg shadow-sm p-6">
				<h2 className="text-2xl font-semibold mb-6">Key Concepts</h2>
				<div className="space-y-4">
					{concepts && concepts?.map((concept, index) => (
						<div
							key={index}
							className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
							onClick={() => handleConceptClick(concept)}
						>
							<div className="flex items-center gap-3">
								<Book className="text-blue-600" size={24} />
								<span className="font-medium">{concept?.content}</span>
							</div>
							<ChevronRight className="text-gray-400" size={20} />
						</div>
					))}
				</div>
			</div>

			<Dialog
				open={isDialogOpen}
				onOpenChange={setIsDialogOpen}
				title={selectedConcept?.content}
			>
				<p className="text-gray-700 leading-relaxed">
					{selectedConcept.explanation}
				</p>
			</Dialog>
		</div>
	);
};

export default ConceptPage;
