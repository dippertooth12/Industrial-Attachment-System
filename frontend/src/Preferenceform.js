import React, { useState } from 'react';

const StudentPreferenceForm = () => {
  const [formData, setFormData] = useState({
    student_id: '',
    student_pref_id: '',
    pref_location: '',
    available_from: '',
    available_to: ''
  });

  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    try {
      const response = await fetch('/api/preferences/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSuccess(true);
        setFormData({
          student_id: '',
          student_pref_id: '',
          pref_location: '',
          available_from: '',
          available_to: '',
        });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Something went wrong.');
      }
    } catch (err) {
      setError('Server error. Try again later.');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white shadow-md rounded-xl">
      <h2 className="text-xl font-bold mb-4">Student Preference Form</h2>
      {success && <p className="text-green-600">Submitted successfully!</p>}
      {error && <p className="text-red-600">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="student_id"
          placeholder="Student ID"
          value={formData.student_id}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <input
          name="student_pref_id"
          placeholder="Preference ID"
          value={formData.student_pref_id}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <input
          name="pref_location"
          placeholder="Preferred Location"
          value={formData.pref_location}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <label className="block">Available From:</label>
        <input
          name="available_from"
          type="date"
          value={formData.available_from}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <label className="block">Available To:</label>
        <input
          name="available_to"
          type="date"
          value={formData.available_to}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default StudentPreferenceForm;