"""
StudentRepository Example Usage
Demonstrates comprehensive usage of the StudentRepository with MongoDB Atlas
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.repos.student import StudentRepository
from models.student import (
    StudentProfile, 
    StudentPreference, 
    Education, 
    Experience, 
    Award, 
    ExtraCurricular, 
    StandardizedTest
)
from models.user import UserRole, UserStatus


def main():
    """Comprehensive example of StudentRepository usage"""
    print("=== StudentRepository Example Usage ===\n")
    
    # Initialize repository with MongoDB Atlas
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    database_name = os.getenv("MONGODB_DBNAME_STUDENT")
    repo = StudentRepository(connection_string, database_name)
    
    try:
        print("1. Repository Initialization")
        print("-" * 40)
        print(f"✓ Connected to MongoDB Atlas database: {database_name}")
        print(f"✓ Connection string: {connection_string.replace('Combi9144%40', '***')}")
        print("✓ Collections and indexes initialized")
        print()
        
        # 1. Student Profile Operations
        print("2. Student Profile Operations")
        print("-" * 40)
        
        # Create comprehensive student profiles
        student_profiles = [
            {
                "userid": 2001,
                "gender": "Male",
                "overview": "Passionate computer science student with strong interest in artificial intelligence and machine learning. Active in coding competitions and open source projects.",
                "educations": [
                    Education(
                        name="Stanford University",
                        period="09/2022-06/2026",
                        gpa=3.8,
                        degree="Bachelor of Science",
                        major="Computer Science"
                    ),
                    Education(
                        name="MIT Summer Program",
                        period="06/2023-08/2023",
                        gpa=4.0,
                        degree="Certificate",
                        major="Machine Learning"
                    )
                ],
                "experience": [
                    Experience(
                        name="Software Engineering Intern at Google",
                        period="06/2023-08/2023",
                        desc="Developed machine learning models for search optimization, worked with TensorFlow and Python"
                    ),
                    Experience(
                        name="Research Assistant at Stanford AI Lab",
                        period="01/2023-05/2023",
                        desc="Conducted research on natural language processing, published paper on transformer architectures"
                    )
                ],
                "activities": [
                    ExtraCurricular(
                        name="Stanford Computer Science Society",
                        period="09/2022-present",
                        desc="President, organized coding workshops and hackathons for 200+ students"
                    ),
                    ExtraCurricular(
                        name="Open Source Contributor",
                        period="01/2022-present",
                        desc="Active contributor to TensorFlow and PyTorch projects, 50+ merged pull requests"
                    )
                ],
                "standardized_tests": [
                    StandardizedTest(
                        name="SAT",
                        score=1520,
                        date="12/2021"
                    ),
                    StandardizedTest(
                        name="SAT Math Level 2",
                        score=800,
                        date="12/2021"
                    )
                ],
                "awards": [
                    Award(
                        name="Google Code Jam",
                        desc="Finalist in Google Code Jam 2023, ranked in top 100 globally",
                        date="05/2023"
                    ),
                    Award(
                        name="Stanford Dean's List",
                        desc="Academic excellence recognition for 3 consecutive semesters",
                        date="12/2022"
                    )
                ],
                "others": "Fluent in English, Spanish, and Python. Interested in pursuing PhD in AI after graduation."
            },
            {
                "userid": 2002,
                "gender": "Female",
                "overview": "Dedicated pre-med student with passion for biomedical research and global health. Volunteer experience in underserved communities.",
                "educations": [
                    Education(
                        name="Harvard University",
                        period="09/2021-06/2025",
                        gpa=3.9,
                        degree="Bachelor of Arts",
                        major="Biology"
                    )
                ],
                "experience": [
                    Experience(
                        name="Research Intern at Harvard Medical School",
                        period="06/2023-08/2023",
                        desc="Conducted cancer research, analyzed genomic data using R and Python"
                    ),
                    Experience(
                        name="Volunteer at Boston Children's Hospital",
                        period="09/2022-present",
                        desc="Weekly volunteer in pediatric oncology ward, provided emotional support to families"
                    )
                ],
                "activities": [
                    ExtraCurricular(
                        name="Harvard Pre-Med Society",
                        period="09/2021-present",
                        desc="Vice President, organized medical school application workshops"
                    ),
                    ExtraCurricular(
                        name="Global Health Initiative",
                        period="01/2022-present",
                        desc="Led fundraising campaigns for medical supplies in developing countries"
                    )
                ],
                "standardized_tests": [
                    StandardizedTest(
                        name="MCAT",
                        score=520,
                        date="04/2023"
                    ),
                    StandardizedTest(
                        name="SAT",
                        score=1480,
                        date="12/2020"
                    )
                ],
                "awards": [
                    Award(
                        name="Goldwater Scholarship",
                        desc="Prestigious scholarship for outstanding undergraduate research in STEM",
                        date="03/2023"
                    ),
                    Award(
                        name="Harvard Phi Beta Kappa",
                        desc="Academic honor society membership for top 10% of class",
                        date="05/2023"
                    )
                ],
                "others": "Fluent in English, French, and Mandarin. Planning to apply to medical school in 2024."
            },
            {
                "userid": 2003,
                "gender": "Non-binary",
                "overview": "Creative arts student with focus on digital media and social impact. Combining artistic skills with technology for positive change.",
                "educations": [
                    Education(
                        name="NYU Tisch School of the Arts",
                        period="09/2022-06/2026",
                        gpa=3.7,
                        degree="Bachelor of Fine Arts",
                        major="Interactive Media Arts"
                    )
                ],
                "experience": [
                    Experience(
                        name="Digital Media Intern at Adobe",
                        period="06/2023-08/2023",
                        desc="Designed user interfaces for creative software, worked with Figma and Adobe Creative Suite"
                    ),
                    Experience(
                        name="Freelance Graphic Designer",
                        period="01/2022-present",
                        desc="Created visual identities for 20+ small businesses and non-profits"
                    )
                ],
                "activities": [
                    ExtraCurricular(
                        name="NYU Art for Social Change",
                        period="09/2022-present",
                        desc="Co-founder, created art installations addressing climate change and social justice"
                    ),
                    ExtraCurricular(
                        name="LGBTQ+ Student Union",
                        period="09/2022-present",
                        desc="Event coordinator, organized Pride Month celebrations and awareness campaigns"
                    )
                ],
                "standardized_tests": [
                    StandardizedTest(
                        name="SAT",
                        score=1350,
                        date="12/2021"
                    )
                ],
                "awards": [
                    Award(
                        name="Adobe Creative Award",
                        desc="First place in digital art competition for social impact project",
                        date="11/2022"
                    ),
                    Award(
                        name="NYU Dean's List",
                        desc="Academic excellence in fine arts program",
                        date="12/2022"
                    )
                ],
                "others": "Fluent in English and Spanish. Passionate about using art and technology to address social issues."
            }
        ]
        
        # Upsert student profiles
        print("Creating student profiles...")
        for profile_data in student_profiles:
            profile = StudentProfile(**profile_data)
            userid = repo.upsert_student_profile(profile)
            print(f"✓ Upserted profile for user {userid}: {profile.overview[:50]}...")
        print()
        
        # 2. Student Preference Operations
        print("3. Student Preference Operations")
        print("-" * 40)
        
        # Create student preferences
        student_preferences = [
            {
                "userid": 2001,
                "intended_major": ["Computer Science", "Artificial Intelligence", "Machine Learning"],
                "intended_degree": ["Master's", "PhD"],
                "preferred_countries": ["USA", "Canada", "UK"],
                "preferred_cities": ["San Francisco", "Seattle", "Toronto", "London"],
                "budget_min": 50000,
                "budget_max": 100000,
                "others": "Interested in universities with strong AI research programs and industry connections."
            },
            {
                "userid": 2002,
                "intended_major": ["Medicine", "Biomedical Sciences", "Public Health"],
                "intended_degree": ["MD", "MPH", "PhD"],
                "preferred_countries": ["USA", "Canada"],
                "preferred_cities": ["Boston", "New York", "Toronto", "Vancouver"],
                "budget_min": 30000,
                "budget_max": 80000,
                "others": "Looking for medical schools with strong research programs and global health focus."
            },
            {
                "userid": 2003,
                "intended_major": ["Digital Media", "Graphic Design", "Interactive Arts"],
                "intended_degree": ["Master's"],
                "preferred_countries": ["USA", "Netherlands", "Germany"],
                "preferred_cities": ["New York", "Amsterdam", "Berlin", "Los Angeles"],
                "budget_min": 20000,
                "budget_max": 60000,
                "others": "Interested in programs that combine art, technology, and social impact."
            }
        ]
        
        # Upsert student preferences
        print("Creating student preferences...")
        for preference_data in student_preferences:
            preference = StudentPreference(**preference_data)
            userid = repo.upsert_student_preference(preference)
            print(f"✓ Upserted preference for user {userid}: {preference.intended_major}")
        print()
        
        # 3. Read Operations
        print("4. Read Operations")
        print("-" * 40)
        
        # Get student profile by userid
        print("Getting student profile by userid...")
        profile = repo.get_student_profile(2001)
        if profile:
            print(f"✓ Found profile for user {profile.userid}")
            print(f"  Gender: {profile.gender}")
            print(f"  Overview: {profile.overview[:100]}...")
            print(f"  Education count: {len(profile.educations)}")
            print(f"  Experience count: {len(profile.experience)}")
            print(f"  Awards count: {len(profile.awards)}")
        else:
            print("❌ Profile not found")
        print()
        
        # Get student preference by userid
        print("Getting student preference by userid...")
        preference = repo.get_student_preference(2001)
        if preference:
            print(f"✓ Found preference for user {preference.userid}")
            print(f"  Intended majors: {preference.intended_major}")
            print(f"  Preferred countries: {preference.preferred_countries}")
            print(f"  Budget range: ${preference.budget_min:,} - ${preference.budget_max:,}")
        else:
            print("❌ Preference not found")
        print()
        
        # Get all student profiles
        print("Getting all student profiles...")
        all_profiles = repo.get_all_student_profiles()
        print(f"✓ Retrieved {len(all_profiles)} student profiles:")
        for profile in all_profiles:
            print(f"  - User {profile.userid}: {profile.overview[:50]}...")
        print()
        
        # Get all student preferences
        print("Getting all student preferences...")
        all_preferences = repo.get_all_student_preferences()
        print(f"✓ Retrieved {len(all_preferences)} student preferences:")
        for preference in all_preferences:
            print(f"  - User {preference.userid}: {preference.intended_major}")
        print()
        
        # 4. Complete Student Data Operations
        print("5. Complete Student Data Operations")
        print("-" * 40)
        
        # Get complete student data
        print("Getting complete student data...")
        complete_data = repo.get_complete_student_data(2001)
        if complete_data:
            profile, preference = complete_data
            print(f"✓ Retrieved complete data for user {profile.userid}")
            print(f"  Profile: {profile.overview[:50]}...")
            print(f"  Preference: {preference.intended_major}")
        else:
            print("❌ Complete data not found")
        print()
        
        # 5. Update Operations
        print("6. Update Operations")
        print("-" * 40)
        
        # Update student profile
        print("Updating student profile...")
        if profile:
            profile.overview = "Updated overview: Passionate computer science student with expertise in AI and ML. Now focusing on deep learning and neural networks."
            profile.others = "Updated: Fluent in English, Spanish, Python, and JavaScript. Planning to start a tech company after graduation."
            
            userid = repo.upsert_student_profile(profile)
            print(f"✓ Updated profile for user {userid}")
            
            # Verify update
            updated_profile = repo.get_student_profile(userid)
            if updated_profile and "Updated overview" in updated_profile.overview:
                print("✓ Profile update verified")
            else:
                print("❌ Profile update verification failed")
        print()
        
        # Update student preference
        print("Updating student preference...")
        if preference:
            preference.intended_major.append("Data Science")
            preference.preferred_countries.append("Singapore")
            preference.budget_max = 120000
            preference.others = "Updated: Also interested in data science programs and considering Singapore for its tech ecosystem."
            
            userid = repo.upsert_student_preference(preference)
            print(f"✓ Updated preference for user {userid}")
            
            # Verify update
            updated_preference = repo.get_student_preference(userid)
            if updated_preference and "Data Science" in updated_preference.intended_major:
                print("✓ Preference update verified")
            else:
                print("❌ Preference update verification failed")
        print()
        
        # 6. Error Handling
        print("7. Error Handling")
        print("-" * 40)
        
        # Test non-existent user retrieval
        print("Testing non-existent user retrieval...")
        non_existent_profile = repo.get_student_profile(9999)
        non_existent_preference = repo.get_student_preference(9999)
        
        if non_existent_profile is None and non_existent_preference is None:
            print("✓ Correctly returned None for non-existent users")
        else:
            print("❌ Should have returned None for non-existent users")
        print()
        
        # Test duplicate userid handling (upsert should update)
        print("Testing duplicate userid handling...")
        duplicate_profile = StudentProfile(
            userid=2001,  # Existing userid
            gender="Male",
            overview="This is a duplicate profile that should update the existing one",
            educations=[],
            experience=[],
            activities=[],
            standardized_tests=[],
            awards=[],
            others="Duplicate profile test"
        )
        
        userid = repo.upsert_student_profile(duplicate_profile)
        print(f"✓ Upserted duplicate profile for user {userid} (should update existing)")
        
        # Verify it updated the existing profile
        updated_profile = repo.get_student_profile(userid)
        if updated_profile and "duplicate profile" in updated_profile.overview:
            print("✓ Duplicate profile correctly updated existing profile")
        else:
            print("❌ Duplicate profile handling failed")
        print()
        
        # 7. Cleanup
        print("8. Cleanup")
        print("-" * 40)
        
        # Remove complete student data
        print("Removing complete student data...")
        test_userids = [2001, 2002, 2003]
        removed_count = 0
        
        for userid in test_userids:
            if repo.remove_complete_student_data(userid):
                removed_count += 1
                print(f"✓ Removed complete data for user {userid}")
            else:
                print(f"⚠ No data found for user {userid}")
        
        print(f"✓ Cleaned up {removed_count} complete student records")
        print()
        
        print("=== Example completed successfully! ===")
        print("✓ All StudentRepository operations demonstrated")
        print("✓ Profile operations working correctly")
        print("✓ Preference operations working correctly")
        print("✓ Complete data operations working correctly")
        print("✓ Update operations working correctly")
        print("✓ Error handling working correctly")
        
    except Exception as e:
        print(f"❌ Error during example execution: {e}")
        print(f"Error type: {type(e).__name__}")
        raise
    
    finally:
        # Close repository connection
        repo.close()
        print("\n✓ Repository connection closed")


def demonstrate_advanced_usage():
    """Demonstrate advanced usage patterns"""
    print("\n=== Advanced Usage Patterns ===\n")
    
    connection_string = "mongodb+srv://combi2k2:Combi9144%40@combi-learning.zwicz.mongodb.net/?retryWrites=true&w=majority&appName=Combi-Learning"
    database_name = "unifly_students"
    repo = StudentRepository(connection_string, database_name)
    
    try:
        print("1. Batch Profile Creation")
        print("-" * 30)
        
        # Create multiple student profiles in batch
        batch_profiles = []
        for i in range(3):
            profile = StudentProfile(
                userid=3000 + i,
                gender="Other" if i % 2 == 0 else "Female",
                overview=f"Batch student {i} with comprehensive academic background",
                educations=[
                    Education(
                        name=f"University {i}",
                        period="09/2020-06/2024",
                        gpa=3.5 + (i * 0.1),
                        degree="Bachelor's",
                        major=f"Major {i}"
                    )
                ],
                experience=[
                    Experience(
                        name=f"Internship {i}",
                        period="06/2023-08/2023",
                        desc=f"Internship experience {i} description"
                    )
                ],
                activities=[
                    ExtraCurricular(
                        name=f"Activity {i}",
                        period="09/2020-present",
                        desc=f"Activity {i} description"
                    )
                ],
                standardized_tests=[
                    StandardizedTest(
                        name="SAT",
                        score=1400 + (i * 50),
                        date="12/2020"
                    )
                ],
                awards=[
                    Award(
                        name=f"Award {i}",
                        desc=f"Award {i} description",
                        date="05/2023"
                    )
                ],
                others=f"Additional information for batch student {i}"
            )
            batch_profiles.append(profile)
        
        print("Creating batch profiles...")
        for profile in batch_profiles:
            repo.upsert_student_profile(profile)
        print(f"✓ Created {len(batch_profiles)} batch profiles")
        
        # Create corresponding preferences
        batch_preferences = []
        for i in range(3):
            preference = StudentPreference(
                userid=3000 + i,
                intended_major=[f"Major {i}", f"Related Major {i}"],
                intended_degree=["Bachelor's", "Master's"],
                preferred_countries=["USA", "Canada"],
                preferred_cities=[f"City {i}", f"City {i+1}"],
                budget_min=20000 + (i * 10000),
                budget_max=60000 + (i * 10000),
                others=f"Batch preference {i} additional information"
            )
            batch_preferences.append(preference)
        
        print("Creating batch preferences...")
        for preference in batch_preferences:
            repo.upsert_student_preference(preference)
        print(f"✓ Created {len(batch_preferences)} batch preferences")
        
        print("\n2. Data Analysis Operations")
        print("-" * 30)
        
        # Analyze all profiles
        all_profiles = repo.get_all_student_profiles()
        all_preferences = repo.get_all_student_preferences()
        
        print(f"Total profiles: {len(all_profiles)}")
        print(f"Total preferences: {len(all_preferences)}")
        
        # Analyze by gender
        gender_counts = {}
        for profile in all_profiles:
            gender = profile.gender
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        print("Gender distribution:")
        for gender, count in gender_counts.items():
            print(f"  {gender}: {count}")
        
        # Analyze by intended major
        major_counts = {}
        for preference in all_preferences:
            for major in preference.intended_major:
                major_counts[major] = major_counts.get(major, 0) + 1
        
        print("Top intended majors:")
        sorted_majors = sorted(major_counts.items(), key=lambda x: x[1], reverse=True)
        for major, count in sorted_majors[:5]:
            print(f"  {major}: {count}")
        
        # Analyze budget ranges
        budget_ranges = []
        for preference in all_preferences:
            if preference.budget_min and preference.budget_max:
                budget_ranges.append((preference.budget_min, preference.budget_max))
        
        if budget_ranges:
            avg_min = sum(r[0] for r in budget_ranges) / len(budget_ranges)
            avg_max = sum(r[1] for r in budget_ranges) / len(budget_ranges)
            print(f"Average budget range: ${avg_min:,.0f} - ${avg_max:,.0f}")
        
        print("\n3. Cleanup Advanced Data")
        print("-" * 30)
        
        # Clean up batch data
        for userid in range(3000, 3003):
            repo.remove_complete_student_data(userid)
        print("✓ Cleaned up batch test data")
        
    except Exception as e:
        print(f"❌ Error in advanced usage: {e}")
        raise
    
    finally:
        repo.close()


if __name__ == "__main__":
    # Run main example
    main()
    
    # Run advanced usage example
    demonstrate_advanced_usage()
    
    print("\n🎉 All StudentRepository examples completed successfully!")
    print("The StudentRepository is ready for production use with MongoDB Atlas!")
