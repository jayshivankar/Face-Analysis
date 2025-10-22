import jsPDF from 'jspdf';

export const generatePDF = (results, faceImage) => {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  let yPos = 20;

  doc.setFillColor(59, 130, 246);
  doc.rect(0, 0, pageWidth, 30, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(24);
  doc.setFont(undefined, 'bold');
  doc.text('Face Health Analysis Report', pageWidth / 2, 18, { align: 'center' });

  yPos = 40;
  doc.setTextColor(0, 0, 0);

  if (faceImage) {
    try {
      const imgWidth = 60;
      const imgHeight = 60;
      const xPos = (pageWidth - imgWidth) / 2;
      doc.addImage(faceImage, 'JPEG', xPos, yPos, imgWidth, imgHeight);
      yPos += imgHeight + 10;
    } catch (error) {
      console.error('Error adding image to PDF:', error);
    }
  }

  doc.setFontSize(18);
  doc.setFont(undefined, 'bold');
  doc.setTextColor(59, 130, 246);
  doc.text('Health Index', 14, yPos);
  yPos += 8;

  doc.setFontSize(12);
  doc.setFont(undefined, 'normal');
  doc.setTextColor(0, 0, 0);
  doc.text(`Overall Score: ${results.health_index.overall_score}/100`, 14, yPos);
  yPos += 6;
  doc.text(`Rating: ${results.health_index.rating}`, 14, yPos);
  yPos += 12;

  doc.setFontSize(18);
  doc.setFont(undefined, 'bold');
  doc.setTextColor(59, 130, 246);
  doc.text('Analysis Results', 14, yPos);
  yPos += 10;

  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.setTextColor(0, 0, 0);

  const sections = [
    { title: 'Age & Gender', content: `Age: ${results.age} years | Gender: ${results.gender}` },
    { title: 'Fatigue Status', content: results.fatigue },
    { title: 'Emotion', content: results.emotion },
    {
      title: 'Facial Symmetry',
      content: results.symmetry.error
        ? results.symmetry.error
        : `Score: ${results.symmetry.asymmetry_score} | ${results.symmetry.predicted_condition}`,
    },
  ];

  if (results.skin_condition) {
    sections.push({ title: 'Skin Condition', content: results.skin_condition });
  }

  sections.forEach((section) => {
    if (yPos > pageHeight - 30) {
      doc.addPage();
      yPos = 20;
    }

    doc.setFont(undefined, 'bold');
    doc.text(section.title, 14, yPos);
    yPos += 6;

    doc.setFont(undefined, 'normal');
    const lines = doc.splitTextToSize(section.content, pageWidth - 28);
    doc.text(lines, 14, yPos);
    yPos += lines.length * 6 + 4;
  });

  if (results.recommendations && results.recommendations.length > 0) {
    if (yPos > pageHeight - 60) {
      doc.addPage();
      yPos = 20;
    }

    yPos += 5;
    doc.setFontSize(18);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(59, 130, 246);
    doc.text('Recommendations', 14, yPos);
    yPos += 10;

    doc.setFontSize(11);
    doc.setFont(undefined, 'normal');
    doc.setTextColor(0, 0, 0);

    results.recommendations.forEach((rec, idx) => {
      if (yPos > pageHeight - 20) {
        doc.addPage();
        yPos = 20;
      }

      const recText = `${idx + 1}. ${rec}`;
      const lines = doc.splitTextToSize(recText, pageWidth - 28);
      doc.text(lines, 14, yPos);
      yPos += lines.length * 5 + 3;
    });
  }

  if (yPos > pageHeight - 30) {
    doc.addPage();
    yPos = 20;
  }

  yPos = pageHeight - 20;
  doc.setFontSize(9);
  doc.setTextColor(128, 128, 128);
  doc.text('Disclaimer: This analysis is for informational purposes only and is not a substitute', 14, yPos);
  yPos += 4;
  doc.text('for professional medical advice, diagnosis, or treatment.', 14, yPos);

  const timestamp = new Date().toLocaleString();
  doc.save(`Face_Health_Report_${timestamp.replace(/[/:,\s]/g, '_')}.pdf`);
};
